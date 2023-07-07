from logging import getLogger

from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from datasets.models import Dataset

from .models import (
    DatasetTemplate,
    DatasetTemplateApplyJob,
    DatasetTemplateApplyPreview,
    DatasetTemplateAttr,
    DatasetApplyPreview,
    DatasetApplyJob,
)
from .serializers import (
    DatasetTemplateApplyJobSerializer,
    DatasetTemplateAttrSerializer,
    DatasetTemplatePreviewSerializer,
    DatasetTemplateSerializer,
)

logger = getLogger(__name__)


class DatasetTempletesViewSet(viewsets.ModelViewSet):
    """
    テンプレートのリストを返します。
    """

    serializer_class = DatasetTemplateSerializer

    def get_queryset(self):
        if self.action == "list":
            user = self.request.user
            queryset = (
                DatasetTemplate.objects.all()
                .filter(Q(created_by_id=user.id) | Q(created_by_id=None))
                .order_by("created_by_id")
                .order_by("-updated_at")
            )
        else:
            queryset = DatasetTemplate.objects.all()

        queryset = queryset.with_attrs()

        # キーワード検索
        keyword = self.request.query_params.get("keyword", None)
        if keyword is not None:
            queryset = queryset.search(keyword)

        return queryset

    @action(detail=False, methods=["post"])
    def by(self, request, pk=None):
        user = self.request.user
        datasetId = self.request.POST.get("datasetId")

        dataset = Dataset.objects.get(pk=datasetId)

        datasetTemplate = DatasetTemplate.create_by_dataset(dataset, user=user)
        datasetTemplate.save()

        serializer = self.get_serializer(datasetTemplate, many=False)

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def me(self, request, pk=None):
        """
        ログインユーザのDatasetTemplate
        """
        user = self.request.user
        queryset = (
            DatasetTemplate.objects.all()
            .with_attrs()
            .prefetch_related("created_by")
            .filter(created_by_id=user.id)
            .order_by("-updated_at")
        )

        keyword = self.request.GET.get("keyword")
        if keyword is not None:
            queryset = queryset.search(keyword)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def apply(self, request):
        """
        変換のリクエスト
        """

        dataset_template_id = request.data.get("dataset_template_id")
        if dataset_template_id is not None:
            job = DatasetApplyJob(
                dataset_id=request.data["dataset_id"],
                dataset_template_id=request.data["dataset_template_id"],
                attr_set=request.data["attr_set"],
                output_name=request.data["output_name"],
                created_by=request.user,
            )
        else:
            job = DatasetTemplateApplyJob(
                dataset_id=request.data["dataset_id"],
                template_id=request.data["template_id"],
                attr_set=request.data["attr_set"],
                output_name=request.data["output_name"],
                created_by=request.user,
            )

        job.create()

        serializer = DatasetTemplateApplyJobSerializer(job)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def previews(self, request):
        """
        プレビュー生成のリクエスト
        """

        dataset_template_id = request.data.get("dataset_template_id")
        if dataset_template_id is not None:
            preview = DatasetApplyPreview(
                dataset_id=request.data["dataset_id"],
                dataset_template_id=request.data["dataset_template_id"],
                attr_set=request.data["attr_set"],
                output_name=request.data["output_name"],
                created_by=request.user,
            )
        else:
            preview = DatasetTemplateApplyPreview(
                dataset_id=request.data["dataset_id"],
                template_id=request.data["template_id"],
                attr_set=request.data["attr_set"],
                output_name=request.data["output_name"],
                created_by=request.user,
            )
        preview.create()

        serializer = DatasetTemplatePreviewSerializer(preview)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DatasetTemplateAttrViewSet(viewsets.ModelViewSet):

    queryset = DatasetTemplateAttr.objects.all()
    serializer_class = DatasetTemplateAttrSerializer
