"""tablelinker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http.response import JsonResponse
from django.urls import include, path

# from config.schema import schema
from dataset_convertors.router import router as dataset_convertor_router
from dataset_templates.router import router as dataset_template_router
from datasets.router import router as dataset_router
from users.router import router as user_router
from graphql_jwt.decorators import jwt_cookie
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt


CORS_ORIGIN_WHITELIST = getattr(settings, "CORS_ORIGIN_WHITELIST", None)


def status(request):
    if request.method == "GET":
        return JsonResponse({"ok": True, "cors": CORS_ORIGIN_WHITELIST,})


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include("dashboard.urls")),
    # path("", RedirectView.as_view(pattern_name="datasets:list")),
    path("", include("users.urls")),
    path("", include("datasets.urls")),
    path("", include("dataset_convertors.urls")),
    path("", include("dataset_templates.urls")),
    # V1 API
    path("api/v1/datasets/", include(dataset_router.urls)),
    path("api/v1/templates/", include(dataset_template_router.urls)),
    path("api/v1/convertors/", include(dataset_convertor_router.urls)),
    path("api/v1/users/", include(user_router.urls)),
    path("status", status, name="status"),
    path("graphql", jwt_cookie(csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True)))),
]

# for File
if not settings.AWS_STORAGE:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
