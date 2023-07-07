from rest_framework import serializers

from datasets.models import DatasetSource


class DatasetSourceSerializer(serializers.ModelSerializer):
    """
    データセットソースシリアライザー
    """

    class Meta:
        model = DatasetSource
        fields = ["site_url", "site_name"]
