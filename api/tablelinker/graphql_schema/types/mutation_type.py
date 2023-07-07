import graphql_jwt
import graphene
from django.dispatch import receiver
from graphql_jwt.refresh_token.signals import refresh_token_rotated

from graphql_schema.mutations import user as users_schema
from graphql_schema.mutations import dataset as dataset_schema
from graphql_schema.mutations import dataset_template as dataset_template_schema
from graphql_schema.mutations import dataset_convertor as dataset_preview_schema


class Mutation(graphene.ObjectType):
    # JWT
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

    # users
    create_user = users_schema.CreateUser.Field()
    update_user = users_schema.UpdateUser.Field()
    password_reset_request = users_schema.PasswordResetRequest.Field()
    password_reset = users_schema.PasswordReset.Field()

    # dataset_group
    create_dataset_group = dataset_schema.CreateDatasetGroup.Field()
    update_dataset_group = dataset_schema.UpdateDatasetGroup.Field()
    delete_dataset_group = dataset_schema.DeleteDatasetGroup.Field()
    analyze_dataset_group = dataset_schema.AnalyzeDatasetGroup.Field()
    change_dataset_current_version = dataset_schema.ChangeDatasetCurrentVersion.Field()

    # dataset
    # 最新のdatasetのみ残してdatasetを消す
    delete_dataset = dataset_schema.DeleteDataset.Field()

    # dataset_attr
    update_dataset_attr = dataset_schema.UpdateDatasetAttr.Field()

    # dataset_template
    create_template_from_dataset_group = dataset_template_schema.CreateTemplateFromDatasetGroup.Field()
    update_template = dataset_template_schema.UpdateTemplate.Field()
    delete_template = dataset_template_schema.DeleteTemplate.Field()
    update_template_attr = dataset_template_schema.UpdateTemplateAttr.Field()

    # convertor
    create_convert_preview = dataset_preview_schema.CreateConvertPreview.Field()
    create_convert_job = dataset_preview_schema.CreateConvertJob.Field()

    @receiver(refresh_token_rotated)
    def revoke_refresh_token(sender, request, refresh_token, **kwargs):
        refresh_token.revoke(request)
