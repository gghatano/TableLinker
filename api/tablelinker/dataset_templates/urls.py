from django.urls import path

from . import views

app_name = "dataset_templates"

urlpatterns = [
    path("datasets/<uuid:pk>/fit", views.FitTemplateView.as_view(), name="fit"),
]
