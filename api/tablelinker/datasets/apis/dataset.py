from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from datasets.models import Dataset, DatasetCurrentVersion
from datasets.serializers import DatasetGroupSerializer, DatasetSerializer, DatasetSimliarSerializer, DatasetUserStarSerializer
from datasets.tasks import analyze_dataset_task


class DatasetViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "star":
            return DatasetUserStarSerializer
        return DatasetSerializer

    def get_queryset(self):
        if self.action == "list":
            queryset = Dataset.objects.all().with_attrs().with_created_by().analyzed().published().latest().distinct()
        else:
            # get など
            queryset = Dataset.objects.all().with_attrs().with_created_by()

        # キーワード検索
        keyword = self.request.query_params.get("keyword", None)
        if keyword is not None:
            queryset = queryset.search(keyword)

        return queryset

    def perform_create(self, serializer):
        current_version = DatasetCurrentVersion()
        current_version.save()

        dataset_group_serializer = DatasetGroupSerializer(
            data=self.request.data, context={"request": self.request, "current_version": current_version}
        )
        dataset_group_serializer.is_valid()
        dataset_group = dataset_group_serializer.save()

        serializer.context["current_version"] = current_version
        serializer.context["dataset_group"] = dataset_group
        dataset = serializer.save()

        # 同期実行
        # dataset.analyze()

        # 非同期実行
        dataset.set_analyze_request()
        analyze_dataset_task.apply_async(args=[str(dataset.id)], countdown=2)

    @action(detail=True, methods=["post"], permission_classes=[])
    def analyze(self, request, pk=None):
        """
        解析処理
        """
        dataset = Dataset.objects.get(pk=pk)

        # TODO: move to perssion class
        if dataset.created_by != request.user:
            raise Exception("not permission error!")

        # 同期実行
        dataset.analyze()

        # 非同期実行
        # analyze_dataset_task.apply_async(args=[str(dataset.id)], countdown=2)

        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

    @action(detail=True)
    def simliars(self, request, pk=None, permission_classes=[]):
        """
        類似検索
        """
        dataset = Dataset.objects.get(pk=pk)

        keyword = self.request.query_params.get("keyword", None)

        simliar_datasets = dataset.simliar_datasets(keyword, limit=100)
        serializer = DatasetSimliarSerializer(simliar_datasets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def me(self, request, pk=None):
        """
        ログインユーザのDataset
        """
        queryset = Dataset.objects.all().with_attrs().with_created_by().by_user(self.request.user).latest()

        keyword = self.request.GET.get("keyword")
        if keyword is not None:
            queryset = queryset.search(keyword)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post", "delete"], permission_classes=[])
    def star(self, request, pk=None):
        instance = self.get_object()

        if request.method == "POST":
            instance.stared_users.add(request.user)
            serializer = DatasetUserStarSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            status_code = status.HTTP_204_NO_CONTENT
            instance.stared_users.remove(request.user)
            return Response(status=status_code)
