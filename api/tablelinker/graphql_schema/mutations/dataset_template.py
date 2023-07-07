import enum
from django.db import transaction

import graphene
from dataset_templates.models import (
    DatasetTemplate,
    DatasetTemplateAttr,
)
from datasets.models import DatasetGroup
from graphql_jwt.decorators import login_required
from graphql_schema.types.objects import (
    DatasetTemplateType,
    UpdateTemplateInputType,
    DatasetTemplateAttrType,
    UpdateTemplateAttrInputType,
)
from users.models import User


class TemplateStatusEnum(enum.Enum):
    FAIL = 0
    SUCCESS = 1


class CreateTemplateFromDatasetGroup(graphene.Mutation):
    class Arguments:
        dataset_group_id = graphene.UUID(required=True)

    dataset_template = graphene.Field(DatasetTemplateType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, **kwargs):
        pk = info.context.user.id
        user = User.objects.get(pk=pk)

        dataset_group = DatasetGroup.objects.get(pk=kwargs["dataset_group_id"])
        dataset = dataset_group.current_dataset

        dataset_template = DatasetTemplate.create_by_dataset(dataset, user=user)
        dataset_template.save()
        return CreateTemplateFromDatasetGroup(dataset_template=dataset_template)


class UpdateTemplate(graphene.Mutation):
    class Arguments:
        input = UpdateTemplateInputType(required=True)

    template = graphene.Field(DatasetTemplateType)

    @login_required
    @transaction.atomic
    def mutate(self, info, **kwargs):
        template = DatasetTemplate.objects.get(pk=kwargs["input"]["template_id"])
        for attr, value in kwargs["input"].items():
            setattr(template, attr, value)
        template.save()

        return UpdateTemplate(template=template)


class DeleteTemplate(graphene.Mutation):
    class Arguments:
        template_id = graphene.UUID(required=True)

    status = graphene.Field(graphene.Enum.from_enum(TemplateStatusEnum))

    @login_required
    @transaction.atomic
    def mutate(self, info, **kwargs):
        template = DatasetTemplate.objects.get(pk=kwargs["template_id"])
        if template.created_by != info.context.user:
            raise Exception("not permission error!")
        template.delete()
        return DeleteTemplate(status=TemplateStatusEnum.SUCCESS)


class UpdateTemplateAttr(graphene.Mutation):
    class Arguments:
        input = UpdateTemplateAttrInputType(required=True)

    template_attr = graphene.Field(DatasetTemplateAttrType)

    @login_required
    @transaction.atomic
    def mutate(self, info, **kwargs):
        template_attr = DatasetTemplateAttr.objects.get(pk=kwargs["input"]["attr_id"])
        if template_attr.dataset_template.created_by != info.context.user:
            raise Exception("not permission error!")
        for attr, value in kwargs["input"].items():
            setattr(template_attr, attr, value)
        template_attr.save()
        return UpdateTemplateAttr(template_attr=template_attr)
