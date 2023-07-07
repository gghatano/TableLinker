from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from datasets.models import Dataset


class ConvertView(LoginRequiredMixin, generic.DetailView):
    model = Dataset
    template_name = "datasets/dataset_convert.html"
