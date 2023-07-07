from django.urls import path

from . import views

app_name = "dataset_convertors"

urlpatterns = [
    path("datasets/<uuid:pk>/convert", views.ConvertView.as_view(), name="convert",),
]
