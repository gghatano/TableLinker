from rest_framework import routers

from . import apis

# api
router = routers.DefaultRouter()
router.register(r"me", apis.UserMeViewSet, basename="")
