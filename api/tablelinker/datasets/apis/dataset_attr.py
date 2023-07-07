from rest_framework import mixins, viewsets

from datasets.models import DatasetAttr
from datasets.serializers import DatasetAttrSerializer


class DatasetAttrViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = DatasetAttr.objects.all()
    serializer_class = DatasetAttrSerializer
