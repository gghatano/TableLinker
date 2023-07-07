import enum
from time import sleep
import graphene
from django.db import transaction
from datasets.models import Dataset, DatasetGroup, DatasetAttr, DatasetCurrentVersion, DatasetSource
from datasets.tasks import analyze_dataset_task
from graphql_jwt.decorators import login_required
from graphql_schema.types.objects import (
    DatasetGroupType,
    CreateDatasetGroupInputType,
    UpdateDatasetGroupInputType,
    AnalyzeDatasetGroupInputType,
    UpdateDatasetAttrInputType,
    DatasetAttrType,
)
from users.models import User


class StatusEnum(enum.Enum):
    FAIL = 0
    SUCCESS = 1


class DatasetDeleteStatusEnum(enum.Enum):
    FAIL = 0
    SUCCESS = 1


class CreateDatasetGroup(graphene.Mutation):
    class Arguments:
        input = CreateDatasetGroupInputType(required=True)

    dataset_group = graphene.Field(DatasetGroupType)

    @login_required
    @transaction.non_atomic_requests
    def mutate(self, info, **kwargs):
        source_data = None
        try:
            source_data = kwargs["input"].pop("source")
        except KeyError:
            pass

        dataset = None
        with transaction.atomic():
            pk = info.context.user.id
            user = User.objects.get(pk=pk)

            dataset_group = DatasetGroup()
            dataset_group.name = kwargs["input"]["name"]
            dataset_group.original_file = kwargs["input"]["original_file"]
            dataset_group.created_by = user

            dataset_group.save()

            dataset = Dataset()
            dataset.name = "アップロードしました。"
            dataset.created_by = user
            dataset.dataset_group = dataset_group
            dataset.save()

            current_version = DatasetCurrentVersion(dataset_group=dataset_group, dataset=dataset)
            current_version.save()

            if source_data is not None:
                DatasetSource.objects.create(dataset_group=dataset_group, **source_data)

            # 同期実行
            # dataset.analyze()

            # 非同期実行
            dataset.set_analyze_request()

            dataset.save()
            dataset.refresh_from_db()

        # JOBQUEで同期的に実行
        # worker = analyze_dataset_task.delay(str(dataset.id))
        # while not worker.ready():
        #      sleep(0.5)

        # JOBQUEで非同期で実行
        analyze_dataset_task.apply_async(args=[str(dataset.id)], countdown=2)
        # analyze_dataset_task.delay(str(dataset.id))

        return CreateDatasetGroup(dataset_group=dataset_group)


class UpdateDatasetGroup(graphene.Mutation):
    class Arguments:
        input = UpdateDatasetGroupInputType(required=True)

    dataset_group = graphene.Field(DatasetGroupType)

    @login_required
    @transaction.atomic
    def mutate(self, info, **kwargs):
        dataset_group = DatasetGroup.objects.get(pk=kwargs["input"]["dataset_group_id"])

        source_data = None
        try:
            source_data = kwargs["input"].pop("source")
        except KeyError:
            pass

        current_dataset = None
        try:
            current_dataset = Dataset.objects.get(pk=kwargs["input"].pop("current_dataset_id"))
        except KeyError:
            pass

        for attr, value in kwargs["input"].items():
            setattr(dataset_group, attr, value)
        dataset_group.save()

        if source_data is not None:
            source_instance = dataset_group.source
            for attr, value in source_data.items():
                setattr(source_instance, attr, value)
            source_instance.save()

        if current_dataset is not None:
            dataset_group.set_current_version(current_dataset)

        return UpdateDatasetGroup(dataset_group=dataset_group)


class DeleteDatasetGroup(graphene.Mutation):
    class Arguments:
        dataset_group_id = graphene.UUID(required=True)

    status = graphene.Field(graphene.Enum.from_enum(StatusEnum))

    @login_required
    @transaction.atomic
    def mutate(self, info, **kwargs):
        dataset_group = DatasetGroup.objects.get(pk=kwargs["dataset_group_id"])
        if dataset_group.created_by != info.context.user:
            raise Exception("not permission error!")
        dataset_group.delete()
        return DeleteDatasetGroup(status=StatusEnum.SUCCESS)


class DeleteDataset(graphene.Mutation):
    class Arguments:
        dataset_group_id = graphene.UUID(required=True)

    status = graphene.Field(graphene.Enum.from_enum(DatasetDeleteStatusEnum))

    @login_required
    @transaction.atomic
    def mutate(self, info, **kwargs):
        dataset_group = DatasetGroup.objects.get(pk=kwargs["dataset_group_id"])
        if dataset_group.created_by != info.context.user:
            raise Exception("not permission error!")
        for dataset in dataset_group.dataset.filter(current_version_id__isnull=True):
            dataset.delete()
        return DeleteDataset(status=DatasetDeleteStatusEnum.SUCCESS)


class ChangeDatasetCurrentVersion(graphene.Mutation):
    class Arguments:
        dataset_group_id = graphene.UUID(required=True)
        version = graphene.Int(required=True)

    dataset_group = graphene.Field(DatasetGroupType)

    @login_required
    @transaction.atomic
    def mutate(self, info, **kwargs):
        dataset_group = DatasetGroup.objects.get(pk=kwargs["dataset_group_id"])
        if dataset_group.created_by != info.context.user:
            raise Exception("not permission error!")

        target_dataset = dataset_group.dataset.filter(version=kwargs["version"]).first()
        if not target_dataset:
            raise Exception("target not found error!")

        current_dataset = dataset_group.current_dataset
        target_dataset.current_version = current_dataset.current_version
        current_dataset.current_version = None
        current_dataset.save()
        target_dataset.save()

        return ChangeDatasetCurrentVersion(dataset_group=dataset_group)


class AnalyzeDatasetGroup(graphene.Mutation):
    class Arguments:
        input = AnalyzeDatasetGroupInputType(required=True)

    dataset_group = graphene.Field(DatasetGroupType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, **kwargs):
        """
        解析処理
        """
        dataset_group = DatasetGroup.objects.get(pk=kwargs["input"]["dataset_group_id"])
        dataset = dataset_group.current_dataset

        # TODO: move to perssion class
        if dataset_group.created_by != info.context.user:
            raise Exception("not permission error!")

        # 同期実行
        # dataset.analyze()

        # 非同期実行
        # analyze_dataset_task.apply_async(args=[str(dataset.id)], countdown=2)
        worker = analyze_dataset_task.delay(str(dataset.id), convert=True)
        while not worker.ready():
            sleep(0.5)

        return AnalyzeDatasetGroup(dataset_group=dataset_group)


class UpdateDatasetAttr(graphene.Mutation):
    class Arguments:
        input = UpdateDatasetAttrInputType(required=True)

    dataset_attr = graphene.Field(DatasetAttrType)

    @login_required
    @transaction.atomic
    def mutate(self, info, **kwargs):
        dataset_attr = DatasetAttr.objects.get(pk=kwargs["input"]["attr_id"])
        if dataset_attr.dataset.created_by != info.context.user:
            raise Exception("not permission error!")
        for attr, value in kwargs["input"].items():
            setattr(dataset_attr, attr, value)
        dataset_attr.save()
        return UpdateDatasetAttr(dataset_attr=dataset_attr)
