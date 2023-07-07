import uuid

from django.db import models

from .dataset import DatasetGroup


class DatasetSource(models.Model):
    """
    データセットの取得元の情報
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset_group = models.OneToOneField(DatasetGroup, on_delete=models.CASCADE, related_name="source", default=None)

    site_name = models.CharField(verbose_name="サイト名", null=True, blank=True, max_length=128)
    site_url = models.URLField(verbose_name="サイトURL", null=True, blank=True)

    def is_empty(self):
        return self.site_name is None and self.site_url is None

    def __str__(self):
        return self.site_name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["dataset_group"], name="unique_dataset_source_dataset_group"),
        ]
