import json

from rest_framework import serializers

from datasets.models import DatasetAttr
from datasets.models.attr_type import AttrType


class DatasetAttrSerializer(serializers.ModelSerializer):
    """
    データセット属性シリアライザー
    """

    name = serializers.CharField(read_only=True)
    index = serializers.IntegerField(read_only=True)
    attr_type = serializers.CharField(required=False)
    attr_type_name = serializers.CharField(read_only=True)
    sample_values = serializers.SerializerMethodField()

    class Meta:
        model = DatasetAttr
        fields = [
            "id",
            "name",
            "data_type",
            "attr_type",
            "attr_type_name",
            "sample_values",
            "index",
        ]

    def get_sample_values(self, obj):
        if obj.sample_values is None:
            return []
        return json.loads(obj.sample_values)

    def update(self, instance, validated_data):

        attr_type_id = validated_data.get("attr_type_id", None)
        if attr_type_id is not None:
            attr_type = AttrType.objects.get(pk=attr_type_id)
            if attr_type is None:
                raise serializers.ValidationError("attr_type not found.")
            validated_data["attr_type"] = attr_type

        if "attr_type_id" in validated_data:
            del validated_data["attr_type_id"]

        return super().update(instance, validated_data)
