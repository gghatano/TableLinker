import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from datasets.models import DatasetSource
from users.models import User
import json


class DataTypeType(graphene.Enum):
    unknown = "unknown"
    string = "string"
    integer = "integer"
    float = "float"
    datetime = "datetime"
    boolean = "boolean"
    uri = "uri"


class AttrTypeType(graphene.Enum):
    unknown = "unknown"
    blank = "blank"
    person = "person"
    contact = "contact"
    organization = "organization"
    location = "location"
    model_number = "model_number"
    facility_name = "facility_name"
    weight = "weight"
    price = "price"
    date = "date"
    tel = "tel"
    count_of_people = "count_of_people"
    coordinate = "coordinate"
    event = "event"
    quantity = "quantity"
    length = "length"
    term = "term"
    address = "address"
    area = "area"
    datetime = "datetime"


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "name", "email")


class DatasetCurrentVersionType(graphene.ObjectType):
    id = graphene.String()


class DatasetAttrType(graphene.ObjectType):
    id = graphene.UUID()
    dataset_id = graphene.String()
    name = graphene.String()
    index = graphene.Int()
    no = graphene.Int()
    attr_type = graphene.Field(AttrTypeType)
    attr_type_name = graphene.String()
    data_type = graphene.Field(DataTypeType)
    data_type_name = graphene.String()
    sample_values = graphene.List(graphene.String)

    def resolve_sample_values(parent, info):
        if parent.sample_values is not None:
            return json.loads(parent.sample_values)
        else:
            return None

    def resolve_no(parent, info):
        return parent.index + 1


class DatasetType(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    dataset_group_id = graphene.String()
    current_version = graphene.Field(DatasetCurrentVersionType)
    num_records = graphene.Int()
    num_columns = graphene.Int()
    file_size = graphene.Int()
    filter_json = graphene.String()
    filter_detail = graphene.String()
    attr_names = graphene.List(graphene.String)
    attrs = graphene.List(DatasetAttrType)
    data_file = graphene.String()
    data_file_url = graphene.String()
    analyzed_status = graphene.Int()
    analyzed_at = graphene.DateTime()
    is_analyzed = graphene.Boolean()
    has_annotates = graphene.Boolean()
    annotate_messages = graphene.List(graphene.String)
    encoding = graphene.String()
    version = graphene.Int()
    created_by = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()


class DatasetSourceType(DjangoObjectType):
    class Meta:
        model = DatasetSource


class DatasetGroupType(graphene.ObjectType):
    id = graphene.String()
    current_dataset = graphene.Field(DatasetType)
    current_version = graphene.Field(DatasetCurrentVersionType)
    datasets = graphene.List(DatasetType)

    name = graphene.String()
    public_level = graphene.Int()
    public_level_name = graphene.String()
    encoding = graphene.String()
    source = graphene.Field(DatasetSourceType)
    original_file = graphene.String()
    created_by = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    is_owner = graphene.Boolean()

    def resolve_datasets(parent, info):
        return parent.datasets.all().order_by("-version")

    def resolve_is_owner(parent, info):
        return parent.created_by.id == info.context.user.id


class DatasetGroupListType(graphene.ObjectType):
    dataset_groups = graphene.List(DatasetGroupType)
    total_records = graphene.Int()
    keyword = graphene.String(required=False)
    page = graphene.Int(required=False)
    page_size = graphene.Int(required=False)


class EnumType(graphene.ObjectType):
    name = graphene.String()
    value = graphene.String()


class DatasetTemplateAttrType(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    index = graphene.Int()
    no = graphene.Int()
    desc = graphene.String()
    attr_type = graphene.Field(AttrTypeType)
    attr_type_name = graphene.String()
    data_type = graphene.Field(DataTypeType)
    data_type_name = graphene.String()
    sample_values = graphene.List(graphene.String)

    def resolve_no(parent, info):
        return parent.index + 1


class DatasetTemplateType(graphene.ObjectType):
    id = graphene.UUID()
    name = graphene.String()
    desc = graphene.String()
    attrs = graphene.List(DatasetTemplateAttrType)
    source_dataset = graphene.Field(DatasetType)


class ParamType(graphene.ObjectType):
    name = graphene.String()
    description = graphene.String()
    help_text = graphene.String()
    group = graphene.String()
    default_value = graphene.String()
    label = graphene.String()
    required = graphene.Boolean()
    type = graphene.String()
    arguments = GenericScalar()


class FilterType(graphene.ObjectType):
    key = graphene.String()
    name = graphene.String()
    description = graphene.String()
    help_text = graphene.String()
    params = graphene.List(ParamType)


class DatasetPreviewType(graphene.ObjectType):
    dataset = graphene.Field(DatasetType)
    filter_key = graphene.String()
    task_id = graphene.String()
    result = graphene.String()
    status = graphene.String()
    has_error = graphene.Boolean()
    errors = GenericScalar()
    error_messages = graphene.List(graphene.String)


class DatasetConvertJobType(graphene.ObjectType):
    dataset = graphene.Field(DatasetType)
    filter_key = graphene.String()
    output_name = graphene.String()
    task_id = graphene.String()
    result = graphene.String()
    status = graphene.String()
    has_error = graphene.String()
    errors = GenericScalar()
    error_messages = graphene.List(graphene.String)


class SimilarDatasetType(graphene.ObjectType):
    sim = graphene.Float()
    dataset_group = graphene.Field(DatasetGroupType)


class TemplateInputType(graphene.InputObjectType):
    dataset_template_id = graphene.UUID(required=False)
    dataset_group_id = graphene.UUID(required=True)
    attr_set = GenericScalar(required=True)
    output_name = graphene.String(required=True)
    template_id = graphene.UUID(required=False)


class DatasetSourceInputType(graphene.InputObjectType):
    site_name = graphene.String(required=False)
    site_url = graphene.String(required=False)


class CreateUserInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class UpdateUserInputType(graphene.InputObjectType):
    name = graphene.String(required=False)
    email = graphene.String(required=False)
    password = graphene.String(required=False)


class CreateDatasetGroupInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
    original_file = Upload(required=True)
    source = graphene.Field(DatasetSourceInputType)


class UpdateDatasetGroupInputType(graphene.InputObjectType):
    dataset_group_id = graphene.UUID(required=True)
    name = graphene.String(required=False)
    public_level = graphene.Int(required=False)
    original_file = Upload(required=False)
    created_by = graphene.String(required=False)
    source = graphene.Field(DatasetSourceInputType, required=False)
    current_dataset_id = graphene.UUID(required=False)


class AnalyzeDatasetGroupInputType(graphene.InputObjectType):
    dataset_group_id = graphene.UUID(required=True)


class UpdateTemplateInputType(graphene.InputObjectType):
    template_id = graphene.UUID(required=True)
    name = graphene.String(required=False)
    desc = graphene.String(required=False)


class UpdateTemplateAttrInputType(graphene.InputObjectType):
    attr_id = graphene.UUID(required=True)
    name = graphene.String(required=False)
    index = graphene.Int(required=False)
    desc = graphene.String(required=False)
    data_type = graphene.Field(DataTypeType, required=False)
    attr_type = graphene.Field(AttrTypeType, required=False)


class UpdateDatasetAttrInputType(graphene.InputObjectType):
    attr_id = graphene.UUID(required=True)
    name = graphene.String(required=False)
    index = graphene.Int(required=False)
    data_type = graphene.Field(DataTypeType, required=False)
    attr_type = graphene.Field(AttrTypeType, required=False)


class CreateConvertJobInputType(graphene.InputObjectType):
    dataset_group_id = graphene.UUID(required=True)
    filter_key = graphene.String(required=True)
    filter_params = graphene.String(required=True)


class CreatePreviewInputType(graphene.InputObjectType):
    dataset_group_id = graphene.UUID(required=True)
    filter_key = graphene.String(required=True)
    filter_params = graphene.String(required=True)


# データセットグループへのサジェスト
class ConvertSuggestType(graphene.ObjectType):
    title = graphene.String(description="変換の短い文字列")
    message = graphene.String(description="メッセージ")
    source_index = graphene.Int(description="インデックス")
    filter_key = graphene.String(required=True)
    filter_params = graphene.String(required=True)


# データセットグループへのサジェスト
class SuggestDatasetGroupType(graphene.ObjectType):
    id = graphene.String()
    dataset_group = graphene.Field(DatasetGroupType)
    target_dataset_group = graphene.Field(DatasetGroupType)
    suggests = graphene.List(ConvertSuggestType)


# データセットテンプレートへのサジェスト
class SuggestDatasetTemplateType(graphene.ObjectType):
    id = graphene.String()
    dataset_group = graphene.Field(DatasetGroupType)
    target_dataset_template = graphene.Field(DatasetTemplateType)
    suggests = graphene.List(ConvertSuggestType)
