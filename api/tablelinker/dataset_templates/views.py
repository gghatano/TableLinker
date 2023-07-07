from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from datasets.models import Dataset


class FitTemplateView(LoginRequiredMixin, generic.DetailView):
    model = Dataset
    template_name = "dataset_templates/dataset_fit_template.html"
