import codecs
from logging import getLogger
import urllib.parse

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
import jwt

from .forms import DatasetCreateForm, DatasetSourceForm, DatasetUpdateForm
from .models import Dataset
from .tasks import analyze_dataset_task

logger = getLogger(__name__)


class ListView(LoginRequiredMixin, generic.ListView):
    model = Dataset
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.all().with_attrs().with_created_by().analyzed().published().latest().distinct()

        # キーワード検索
        # TODO: 項目検索
        keyword = self.request.GET.get("keyword")
        if keyword is not None:
            queryset = queryset.search(keyword)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["keyword"] = self.request.GET.get("keyword")
        context["keyword"] = self.request.GET.get("keyword")
        return context


class MyListView(LoginRequiredMixin, generic.ListView):
    model = Dataset
    paginate_by = 10
    template_name = "datasets/dataset_mylist.html"

    def get_queryset(self):
        queryset = self.model.objects.all().with_attrs().with_created_by().by_user(self.request.user).latest()

        # キーワード検索
        # TODO: 項目検索
        keyword = self.request.GET.get("keyword")
        if keyword is not None:
            queryset = queryset.search(keyword)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["keyword"] = self.request.GET.get("keyword")
        return context


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Dataset
    form_class = DatasetCreateForm

    def get_success_url(self):
        return reverse("datasets:detail", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None

        form = self.get_form()
        dataset_form = DatasetSourceForm(data=self.request.POST)
        if form.is_valid():
            return self.form_valid(form, dataset_form)
        else:
            return self.form_invalid(form, dataset_form)

    def form_valid(self, form, datasource_form):
        dataset = form.save(commit=False)
        dataset.created_by = self.request.user
        dataset.save()

        dataset_source = datasource_form.save(commit=False)
        if not dataset_source.is_empty():
            dataset_source.dataset = dataset
            dataset_source.save()

        # 同期実行
        # dataset.analyze()

        # 非同期実行
        analyze_dataset_task.apply_async(args=[str(dataset.id)], countdown=10, expires=3600)

        self.object = dataset

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # contextは辞書型
        context.update(
            {"datase_source_form": DatasetSourceForm(**self.get_form_kwargs()), }
        )
        return context


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Dataset
    queryset = Dataset.objects.all().with_attrs().with_created_by()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        dataset = ctx["dataset"]
        ctx["stared"] = "true" if dataset.is_stared(self.request.user) else "false"
        return ctx


@method_decorator(csrf_exempt, name="dispatch")
class DownloadView(View):

    def get(self, _request, token):
        secret = settings.SECRET_KEY
        jwt_token = token

        payload = jwt.decode(jwt_token, secret, algorithms=["HS256"])
        dataset_id = payload["dataset_id"]
        dataset = Dataset.objects.all().with_attrs().analyzed().get(pk=dataset_id)

        response = HttpResponse(content_type="text/csv")
        filename = dataset.dataset_group.name
        quoted_filename = urllib.parse.quote(filename)
        response["Content-Disposition"] = (
            f"attachment; filename = {quoted_filename}.csv; "
            f"filename* = {quoted_filename}.csv")

        response.write(codecs.BOM_UTF8)  # 内部ファイルは UTF-8 なので BOM を付ける

        for chunk in dataset.data_file:
            response.write(chunk)

        return response


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dataset
    form_class = DatasetUpdateForm

    def get_success_url(self):
        return reverse("datasets:detail", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        dataset = form.save(commit=False)
        dataset.created_by = self.request.user
        self.object = dataset.save()
        return super().form_valid(form)


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dataset
    success_url = "/datasets"
