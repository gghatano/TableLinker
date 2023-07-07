from rest_framework import routers

from . import apis

# api
router = routers.DefaultRouter()
router.register(r"types", apis.AttrTypeViewSet, basename="types")  # TODO権限
router.register(r"attrs", apis.DatasetAttrViewSet)
router.register(r"", apis.DatasetViewSet, basename="")
