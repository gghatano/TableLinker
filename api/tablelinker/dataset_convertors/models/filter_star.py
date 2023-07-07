import uuid

from django.db import models
from rest_framework import serializers

from convertors.core import filter_find_by, filter_keys
from shared.models import TimeStampedModel
from users.models import User


class FilterStar(TimeStampedModel):
    """
    データセットのスター
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filter_key = models.CharField(verbose_name="フィルターID", max_length=128, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stared_fitlers")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["filter_key", "user"], name="unique_filter_key_user_star",),
        ]

    def validate_filter_key(self, filter_key):
        if filter_key not in filter_keys():
            raise serializers.ValidationError("unknown filter key")
        return filter_key

    @property
    def filter(self):
        # TODO: memorize
        return filter_find_by(self.filter_key)

    @property
    def filter_meta(self):
        return self.filter.Meta
