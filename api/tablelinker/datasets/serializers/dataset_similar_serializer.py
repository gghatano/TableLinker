from rest_framework import serializers

from .dataset_serializer import DatasetSerializer


class DatasetSimliarSerializer(serializers.Serializer):
    """
    データセット類似検索シリアライザー
    """

    dataset_id = serializers.SerializerMethodField()
    dataset = DatasetSerializer()
    sim = serializers.FloatField()

    def get_dataset_id(self, obj):
        return obj.dataset.id
