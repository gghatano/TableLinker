import enum
from django.db import transaction
import graphene
import json
from dataset_convertors.models import DatasetConvertJob
from datasets.models import DatasetGroup
from dataset_convertors.models.dataset_preview import DatasetPreview
from graphql_jwt.decorators import login_required
from graphql_schema.types.objects import (
    DatasetPreviewType,
    DatasetConvertJobType,
    CreateConvertJobInputType,
    CreatePreviewInputType,
)
from graphql import GraphQLError


class PreviewStatusEnum(enum.Enum):
    FAIL = 0
    SUCCESS = 1


class CreateConvertPreview(graphene.Mutation):
    class Arguments:
        input = CreatePreviewInputType(required=True)

    dataset_preview = graphene.Field(DatasetPreviewType)
    status = graphene.Field(graphene.Enum.from_enum(PreviewStatusEnum))

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, **kwargs):
        input = kwargs["input"]
        dataset_group = DatasetGroup.objects.get(pk=input["dataset_group_id"])
        dataset = dataset_group.current_dataset
        dataset_preview = DatasetPreview(
            dataset_id=dataset.id, filter_key=input["filter_key"], filter_params=json.loads(input["filter_params"])
        )
        dataset_preview.create()
        if dataset_preview.is_invalid():
            raise GraphQLError("プレビューを作成できませんでした。", extensions=dataset_preview.errors)
        return CreateConvertPreview(status=PreviewStatusEnum.SUCCESS, dataset_preview=dataset_preview)


class JobStatusEnum(enum.Enum):
    FAIL = 0
    SUCCESS = 1


class CreateConvertJob(graphene.Mutation):
    class Arguments:
        input = CreateConvertJobInputType(required=True)

    dataset_convert_job = graphene.Field(DatasetConvertJobType)
    status = graphene.Field(graphene.Enum.from_enum(JobStatusEnum))

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, **kwargs):
        user = info.context.user

        input = kwargs["input"]
        dataset_group_id = input["dataset_group_id"]
        filter_key = input["filter_key"]
        filter_params = input["filter_params"]

        dataset_group = DatasetGroup.objects.get(pk=dataset_group_id)

        job = DatasetConvertJob(
            dataset_id=dataset_group.current_dataset.id,
            dataset_group_id=dataset_group.id,
            filter_key=filter_key,
            filter_params=json.loads(filter_params),
            created_by=user,
        )
        job.create()

        if job.is_invalid():
            raise GraphQLError("変換できませんでした。", extensions=job.errors)

        return CreateConvertJob(status=JobStatusEnum.SUCCESS, dataset_convert_job=job)
