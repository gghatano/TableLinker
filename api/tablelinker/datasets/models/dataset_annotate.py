import uuid

from django.db import models

from .dataset import Dataset


class DatasetAnnotate(models.Model):
    """
    データセットのバリエーションなどエラー情報を保持するモデル
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="annotate_set")
    message = models.TextField(verbose_name="メッセージ")
