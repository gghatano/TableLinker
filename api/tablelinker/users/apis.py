from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import UserSerializer


class UserMeViewSet(viewsets.ViewSet):
    def list(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
