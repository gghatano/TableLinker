from rest_framework import serializers

from datasets.models import DatasetAnnotate


class DatasetAnnotateSerializer(serializers.ModelSerializer):
    """
    データセット注釈シリアライザー
    """

    class Meta:
        model = DatasetAnnotate
        fields = [
            "id",
            "message",
        ]
