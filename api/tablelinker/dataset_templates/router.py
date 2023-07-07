from rest_framework import routers

from . import apis

# api
router = routers.DefaultRouter()
router.register(r"attrs", apis.DatasetTemplateAttrViewSet)
router.register(r"", apis.DatasetTempletesViewSet, basename="")
