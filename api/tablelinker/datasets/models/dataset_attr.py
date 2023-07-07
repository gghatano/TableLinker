import uuid

from django.db import models

from .dataset import Dataset
from .attr_type import AttrType, AttrTypeResolver
from .data_type import DataType, DataTypeResolver


class DatasetAttrQuerySet(models.QuerySet):
    def by_user(self, user):
        return self.filter(dataset__created_by_id=user.id)


class DatasetAttrManager(models.Manager):
    def get_queryset(self):
        return DatasetAttrQuerySet(self.model, using=self._db)


class DatasetAttr(models.Model):
    """
    データセットの属性データ
    """

    objects = DatasetAttrManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="attr_set")
    name = models.CharField(verbose_name="名前", max_length=128, db_index=True)
    index = models.IntegerField(verbose_name="順序", null=False)
    attr_type = models.CharField(verbose_name="意味型", max_length=128, choices=AttrType.choices(), null=True, default="unknown")
    data_type = models.CharField(verbose_name="データ型", max_length=128, choices=DataType.choices(), null=True, default="unknown")
    sample_values = models.TextField(verbose_name="サンプル値", max_length=1024, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["dataset", "index"], name="unique_dataset_attr",),
        ]

    @property
    def attr_type_name(self):
        for attr in AttrType:
            if attr.name == self.attr_type:
                return attr.value

    @property
    def data_type_name(self):
        for attr in DataType:
            if attr.name == self.data_type:
                return attr.value

    def data_type_resolver(self):
        return DataTypeResolver(self)

    def attr_type_resolver(self):
        return AttrTypeResolver(self)
