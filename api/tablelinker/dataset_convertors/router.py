from rest_framework import routers

from . import apis

# api
router = routers.DefaultRouter()
router.register(r"filters", apis.ConvertorFiltersViewSet, basename="filters")
router.register(r"previews", apis.DatasetConvertPreviewViewSet, basename="preview")
router.register(r"jobs", apis.DatasetConvertJobViewSet, basename="convert-job")
router.register(r"datasets", apis.DatasetViewSet, basename="datasets")
