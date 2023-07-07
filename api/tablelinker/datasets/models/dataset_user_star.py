import uuid

from django.contrib.auth import get_user_model
from django.db import models

from shared.models import TimeStampedModel

from .dataset import Dataset

User = get_user_model()


class DatasetUserStar(TimeStampedModel):
    """
    データセットのスター
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["dataset", "user"], name="unique_dataset_user_star",),
        ]
