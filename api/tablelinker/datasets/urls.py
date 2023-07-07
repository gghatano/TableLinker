from django.urls import path

from . import views

app_name = "datasets"

urlpatterns = [
    path("", views.ListView.as_view(), name="home"),
    path("datasets/", views.ListView.as_view(), name="list"),
    path("datasets/me", views.MyListView.as_view(), name="mylist"),
    path("datasets/new", views.CreateView.as_view(), name="create"),
    path("datasets/<uuid:pk>/", views.DetailView.as_view(), name="detail"),
    path("download/datasets/<str:token>", views.DownloadView.as_view(), name="download"),
    path("datasets/<uuid:pk>/edit", views.UpdateView.as_view(), name="update"),
    path("datasets/<uuid:pk>/delete", views.DeleteView.as_view(), name="delete"),
]
