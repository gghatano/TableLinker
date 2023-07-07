from rest_framework import serializers

from datasets.models import DatasetUserStar


class DatasetUserStarSerializer(serializers.ModelSerializer):
    """
    データセットスターシリアライザー
    """

    class Meta:
        model = DatasetUserStar
        fields = ()
        # read_only_fields = ('dataset_id', 'user_id')
