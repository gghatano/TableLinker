import os
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Max
from django.db.models import Q
from django.utils.text import slugify
from inflector import Inflector
from shared.models import TimeStampedModel

from .mixins.dataset_check import DatasetCheckMixin
from .mixins.dataset_similar_search import DatasetGroupSimilarSearchMixin
from .public_level import PublicLevel

# from .dataset import Dataset

User = get_user_model()


def content_file_name_by_origin(instance, filename):
    # オリジナルファイルのファイル名を取得する
    return "/".join(
        [
            slugify(Inflector().pluralize(instance.__class__.__name__)),
            str(instance.id),
            "%s%s" % ("origin", os.path.splitext(filename)[1]),
        ]
    )


class DatasetGroupQuerySet(models.QuerySet):
    def search(self, keyword):
        return self.icontains_keyword_with_attr_name(keyword).distinct()

    def icontains_keyword_with_attr_name(self, keyword):
        return self.filter(Q(dataset_set__attr_set__name__icontains=keyword) | Q(name__icontains=keyword))

    def published(self):
        return self.filter(public_level=PublicLevel.public.value[0])

    def analyzed(self):
        return self.filter(dataset_set__analyzed_at__isnull=False)

    def latest(self):
        return self.order_by("-updated_at")

    def with_attrs(self):
        return self.prefetch_related("dataset_set__attr_set")

    def with_created_by(self):
        return self.prefetch_related("created_by")

    def by_user(self, user):
        return self.filter(created_by_id=user.id)


class DatasetGroupManager(models.Manager):
    def get_queryset(self):
        return DatasetGroupQuerySet(self.model, using=self._db)

    def search(self, keyword):
        return self.get_queryset().search(keyword)


class DatasetGroup(DatasetGroupSimilarSearchMixin, DatasetCheckMixin, TimeStampedModel):
    """データセットグループモデル"""

    objects = DatasetGroupManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="名前", max_length=128, db_index=True)

    original_file = models.FileField(
        verbose_name="オリジナルファイル",
        upload_to=content_file_name_by_origin,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["csv", "tsv"])],
    )
    public_level = models.IntegerField(
        choices=[x.value for x in PublicLevel], default=PublicLevel.private.value[0], db_index=True,
    )
    created_by = models.ForeignKey(
        User, verbose_name="作成者", on_delete=models.CASCADE, related_name="created_dataset_set_group", db_index=True,
    )
    encoding = models.CharField(verbose_name="文字コード", max_length=128, null=True)

    @property
    def public_level_name(self):
        return PublicLevel.get_name(self.public_level)

    def set_publish(self):
        self.public_level = PublicLevel.public.value[0]

    @property
    def datasets(self):
        return self.dataset_set.all()

    @property
    def current_dataset(self):
        return self.current_version.dataset

    @property
    def max_version(self):
        return self.dataset_set.all().aggregate(Max("version"))["version__max"]

    def set_current_version(self, dataset):
        current_version = self.current_version
        current_version.dataset = dataset
        current_version.save()
