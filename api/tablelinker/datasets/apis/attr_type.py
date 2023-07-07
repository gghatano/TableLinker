from datasets.models.attr_type import AttrType
from datasets.serializers import AttrTypeSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class AttrTypeViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = [attr for attr in AttrType]
        serializer = AttrTypeSerializer(queryset, many=True)
        return Response(serializer.data)
