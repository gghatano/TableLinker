from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from convertors.core.filters import filter_meta_list
from dataset_convertors.models import DatasetConvertJob, DatasetPreview
from dataset_convertors.serializers import DatasetConvertJobSerializer, DatasetPreviewSerializer, FilterSerializer
from datasets.models import Dataset

from . import serializers
from .models import FilterStar


class ConvertorFiltersViewSet(viewsets.ViewSet):
    """
    フィルターのリストを返します。
    """

    def list(self, request):
        # TODO: paging
        attr_names = request.GET.get("attr_names")
        query = request.GET.get("query")

        filters = filter_meta_list(attr_names)

        if query is not None:
            filters = [filter for filter in filters if query in filter.name]

        stared_filter_keys = [f.filter_key for f in FilterStar.objects.filter(user=request.user).only("filter_key")]

        serializer = FilterSerializer(filters, many=True, context={"stared_filter_keys": stared_filter_keys},)
        return Response(serializer.data)

    @action(detail=True, methods=["post", "delete"], name="Star to Filter")
    def star(self, request, pk=None):
        user = request.user
        instance = FilterStar.objects.filter(user=user, filter_key=pk).first()
        if request.method == "POST":
            if instance is None:
                instance = FilterStar(user=user, filter_key=pk)
                instance.save()
            status_code = status.HTTP_201_CREATED
            serializer = FilterSerializer(instance.filter_meta, context={"stared_filter_keys": [pk]})

            return Response(serializer.data, status=status_code)

        elif request.method == "DELETE":
            if instance is not None:
                instance.delete()
            status_code = status.HTTP_204_NO_CONTENT

            return Response(status=status_code)


class DatasetConvertPreviewViewSet(viewsets.ViewSet):
    serializer_class = DatasetPreviewSerializer

    def create(self, request):
        """
        プレビュー生成のリクエスト
        :param request:
        :return:
        """
        dataset_preview = DatasetPreview(
            dataset_id=request.data["dataset_id"],
            filter_key=request.data["filter_key"],
            filter_params=request.data["filter_params"],
        )
        dataset_preview.create()
        serializer = DatasetPreviewSerializer(dataset_preview)
        if dataset_preview.is_invalid():
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)


class DatasetConvertJobViewSet(viewsets.ViewSet):
    serializer_class = DatasetConvertJobSerializer

    def create(self, request):
        """
        変換のリクエスト
        :param request:
        :return:
        """
        job = DatasetConvertJob(
            dataset_id=request.data["dataset_id"],
            filter_key=request.data["filter_key"],
            filter_params=request.data["filter_params"],
            output_name=request.data["output_name"],
            created_by=request.user,
        )
        job.create()

        serializer = DatasetConvertJobSerializer(job)

        if job.is_invalid():
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)


class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    属性のリストを返します。
    """

    queryset = Dataset.objects.all().with_attrs().latest()
    serializer_class = serializers.DatasetSerializer

    def get_queryset(self):
        query = self.request.GET.get("query")
        is_star = self.request.GET.get("is_star")
        queryset = Dataset.objects.all().with_attrs().latest().distinct().prefetch_related("stared_users")

        if is_star == "true":
            queryset = queryset.filter(stared_users=self.request.user)

        if query is not None:
            queryset = queryset.search(query)

        return queryset

    @action(detail=True)
    def attrs(self, request, pk=None):
        instance = self.get_object()
        serializer = serializers.DatasetAttrSerializer(instance.attr_set, many=True)
        return Response(serializer.data)
