import graphene
from convertors.core.filters import filter_meta_list
from dataset_templates.models import DatasetTemplate, DatasetTemplateAttr
from datasets.models.attr_type import AttrType
from datasets.models.data_type import DataType
from datasets.models import Dataset, DatasetGroup, DatasetAttr
from django.db.models import Q
from graphql_jwt.decorators import login_required
from graphql_schema.types.objects import (
    UserType,
    DatasetGroupType,
    DatasetGroupListType,
    DatasetType,
    SimilarDatasetType,
    EnumType,
    DatasetAttrType,
    DatasetTemplateType,
    DatasetTemplateAttrType,
    FilterType,
    SuggestDatasetGroupType,
    SuggestDatasetTemplateType,
)
from users.models import User
from datasets.item_mapping.core import item_mapping


class Query(graphene.ObjectType):

    # User
    own_user = graphene.Field(UserType)

    @login_required
    def resolve_own_user(self, info, **kwargs):
        pk = info.context.user.id
        return User.objects.get(pk=pk)

    # DatasetGroup
    dataset_groups = graphene.Field(
        DatasetGroupListType,
        analyzed=graphene.Boolean(required=False),
        published=graphene.Boolean(required=False),
        latest=graphene.Boolean(required=False),
        keyword=graphene.String(required=False),
        page=graphene.Int(required=False),
        page_size=graphene.Int(required=False),
    )

    @login_required
    def resolve_dataset_groups(
        self, info, analyzed=True, published=True, latest=True, keyword=None, page=0, page_size=20, **kwargs
    ):

        queryset = DatasetGroup.objects.all().with_attrs().with_created_by()
        if analyzed:
            queryset = queryset.analyzed()

        if published:
            queryset = queryset.published()
        else:
            queryset.by_user(info.context.user)  # 非公開の場合は、自分のもののみ

        if latest:
            queryset = queryset.latest()

        if keyword is not None:
            queryset = queryset.search(keyword)

        queryset = queryset.distinct()

        total_records = queryset.count()

        skip = page * page_size
        if skip:
            queryset = queryset[skip:]

        if page_size:
            queryset = queryset[:page_size]

        return DatasetGroupListType(
            dataset_groups=queryset, total_records=total_records, page=page, page_size=page_size, keyword=keyword,
        )

    similar_datasets = graphene.List(
        SimilarDatasetType, dataset_group_id=graphene.String(required=True), keyword=graphene.String(required=False),
    )

    @login_required
    def resolve_similar_datasets(self, info, dataset_group_id, keyword=None, **kwargs):
        """
        類似検索
        """
        dataset_group = DatasetGroup.objects.get(pk=dataset_group_id)
        similar_dataset_groups = dataset_group.simliar_datasets(keyword, limit=100)
        return similar_dataset_groups

    # # DatasetGroup
    dataset_group = graphene.Field(DatasetGroupType, id=graphene.UUID(required=True))

    @login_required
    def resolve_dataset_group(self, info, id, **kwargs):
        return DatasetGroup.objects.all().with_attrs().with_created_by().get(pk=id)

    own_dataset_groups = graphene.Field(
        DatasetGroupListType,
        keyword=graphene.String(required=False),
        page=graphene.Int(required=False),
        page_size=graphene.Int(required=False),
    )

    @login_required
    def resolve_own_dataset_groups(self, info, keyword=None, page=0, page_size=20, **kwargs):
        """
        ログインユーザのDatasetGroup
        """
        queryset = DatasetGroup.objects.all().with_attrs().with_created_by().by_user(info.context.user).latest()

        if keyword is not None:
            queryset = queryset.search(keyword)

        queryset = queryset.distinct()

        skip = page * page_size
        if skip:
            queryset = queryset[skip:]

        if page_size:
            queryset = queryset[:page_size]

        return DatasetGroupListType(
            dataset_groups=queryset, total_records=queryset.count(), page=page, page_size=page_size, keyword=keyword,
        )

    # # DatasetGroup
    dataset = graphene.Field(DatasetType, id=graphene.UUID(required=True))

    @login_required
    def resolve_dataset(self, info, id, **kwargs):
        return Dataset.objects.all().with_attrs().with_created_by().get(pk=id)

    # DatasetAttr
    dataset_attrs = graphene.List(DatasetAttrType)

    @login_required
    def resolve_dataset_attrs(self, info, **kwargs):
        return DatasetAttr.objects.all()

    # DatasetGroupAttr
    dataset_group_attrs = graphene.List(DatasetAttrType)

    @login_required
    def resolve_dataset_group_attrs(self, info, **kwargs):
        # カレントに紐づくものだけ取得する
        return DatasetAttr.objects.prefetch_related("dataset").filter(dataset__current_version_id__isnull=True).all()

    # DatasetTemplate
    templates = graphene.List(
        DatasetTemplateType,
        created_by_id=graphene.Boolean(required=False),
        order_created_by_id=graphene.Boolean(required=False),
        order_updated_at=graphene.Boolean(required=False),
        keyword=graphene.String(required=False),
    )

    own_templates = graphene.List(
        DatasetTemplateType, page=graphene.Int(required=False), page_size=graphene.Int(required=False),
    )

    @login_required
    def resolve_templates(
        self, info, created_by_id=None, order_created_by_id=True, order_updated_at=True, keyword=None, **kwargs
    ):

        queryset = DatasetTemplate.objects.all()

        if created_by_id:
            pk = info.context.user.id
            user = User.objects.get(pk=pk)
            queryset = queryset.filter(Q(created_by_id=user.id) | Q(created_by_id=None))
        if order_created_by_id:
            queryset = queryset.order_by("created_by_id")
        if order_updated_at:
            queryset = queryset.order_by("-updated_at")

        queryset = queryset.with_attrs()

        # キーワード検索
        if keyword is not None and len(keyword) > 0:
          queryset = queryset.search(keyword)

        return queryset

    @login_required
    def resolve_own_templates(self, info, keyword=None, page=0, page_size=20, **kwargs):
        """
        ログインユーザのDatasetTemplate
        """
        pk = info.context.user.id
        user = User.objects.get(pk=pk)

        queryset = (
            DatasetTemplate.objects.all()
            .with_attrs()
            .prefetch_related("created_by")
            .filter(created_by_id=user.id)
            .order_by("-updated_at")
        )

        if keyword is not None:
            queryset = queryset.search(keyword)

        skip = page * page_size
        if skip:
            queryset = queryset[skip:]

        if page_size:
            queryset = queryset[:page_size]

        return queryset

    # DatasetTemplateAttr
    template_attrs = graphene.List(DatasetTemplateAttrType)

    @login_required
    def resolve_template_attrs(self, info, **kwargs):
        return DatasetTemplateAttr.objects.all()

    # AttrType
    attr_types = graphene.List(EnumType)

    @login_required
    def resolve_attr_types(self, info, **kwargs):
        attr_types = []
        for value, name in AttrType.choices():
            target = EnumType()
            target.name = name
            target.value = value
            attr_types.append(target)
        return attr_types

    # DataType
    data_types = graphene.List(EnumType)

    @login_required
    def resolve_data_types(self, info, **kwargs):
        data_types = []
        for value, name in DataType.choices():
            target = EnumType()
            target.name = name
            target.value = value
            data_types.append(target)
        return data_types

    # ConvertorFilters
    convertor_filters = graphene.List(
        FilterType,
        description="変換フィルターを検索します。",
        dataset_attr_ids=graphene.List(graphene.UUID, required=False),
        query=graphene.String(required=False),
    )

    @login_required
    def resolve_convertor_filters(self, info, dataset_attr_ids=[], query=None, **kwargs):

        dataset_attrs = None
        if dataset_attr_ids is not None:
            dataset_attrs = DatasetAttr.objects.all().by_user(info.context.user).filter(id__in=dataset_attr_ids)

        attrs = [{"name": attr.name, "attr_type": attr.attr_type, "data_type": attr.data_type,} for attr in dataset_attrs]
        print(attrs)

        filters = filter_meta_list(attrs)

        if query is not None:
            filters = [filter for filter in filters if query in filter.name]

        return filters

    # ConvertorsDatasets
    convertors_dataset_groups = graphene.List(DatasetGroupType, description="???", query=graphene.String(required=False))

    @login_required
    def resolve_convertors_dataset_groups(self, info, query=None, **kwargs):
        queryset = DatasetGroup.objects.all().with_attrs().latest().distinct()

        if query is not None:
            queryset = queryset.search(query)

        return queryset

    # ConvertorsDatasetsAttrs
    convertors_dataset_group_attrs = graphene.List(DatasetAttrType, dataset_group_id=graphene.UUID(required=True))

    @login_required
    def resolve_convertors_dataset_group_attrs(self, info, dataset_group_id, **kwargs):
        return DatasetGroup.objects.filter(pk=dataset_group_id).with_attrs()[0].current_dataset.attrs

    # Suggest DatasetGroup
    suggest_by_dataset_group = graphene.Field(
        SuggestDatasetGroupType,
        description="データセットグループ向けの変換のサジェストを行います。",
        dataset_group_id=graphene.UUID(required=True),
        target_dataset_group_id=graphene.UUID(required=False),
    )

    @login_required
    def resolve_suggest_by_dataset_group(self, info, dataset_group_id, target_dataset_group_id=None, **kwargs):
        dataset_group = DatasetGroup.objects.all().with_attrs().with_created_by().get(pk=dataset_group_id)

        if target_dataset_group_id is not None:
            target_dataset_group = DatasetGroup.objects.all().with_attrs().with_created_by().get(pk=target_dataset_group_id)
            suggests = item_mapping(dataset_group.current_dataset, target_dataset_group.current_dataset)
        else:
            target_dataset_group = None
            suggests = []

        return SuggestDatasetGroupType(
            id=dataset_group.id, dataset_group=dataset_group, target_dataset_group=target_dataset_group, suggests=suggests,
        )

    # Suggest Template
    suggest_by_dataset_template = graphene.Field(
        SuggestDatasetTemplateType,
        description="テンプレート向けの変換のサジェストを行います。",
        dataset_group_id=graphene.UUID(required=True),
        target_dataset_template_id=graphene.UUID(required=False),
    )

    @login_required
    def resolve_suggest_by_dataset_template(self, info, dataset_group_id, target_dataset_template_id=None, **kwargs):
        dataset_group = DatasetGroup.objects.all().with_attrs().with_created_by().get(pk=dataset_group_id)
        if target_dataset_template_id is not None:
            target_dataset_template = DatasetTemplate.objects.all().with_attrs().get(pk=target_dataset_template_id)
            suggests = item_mapping(dataset_group.current_dataset, target_dataset_template)
        else:
            target_dataset_template = None
            suggests = []

        return SuggestDatasetTemplateType(
            id=dataset_group.id,
            dataset_group=dataset_group,
            target_dataset_template=target_dataset_template,
            suggests=suggests,
        )
