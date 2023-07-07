from rest_framework import serializers

from datasets.serializers import DatasetSerializer
from users.serializers import UserSerializer

from .models import DatasetTemplate, DatasetTemplateAttr


class DatasetTemplateAttrSerializer(serializers.ModelSerializer):
    """
    データセットテンプレート属性シリアライザー
    """

    dataset_template_id = serializers.UUIDField(write_only=True, required=False)
    attr_type = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = DatasetTemplateAttr
        fields = [
            "id",
            "name",
            "index",
            "desc",
            "attr_type",
            "data_type",
            "sample_values",
            "dataset_template_id",
            "index",
        ]

    def get_fields(self, *args, **kwargs):
        fields = super(DatasetTemplateAttrSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get("request", None)
        if request and getattr(request, "method", None) == "PUT":
            fields["name"].required = False
            fields["desc"].required = False
            fields["index"].required = False
        return fields

    def update(self, instance, validated_data):
        if "attr_type" in validated_data:
            validated_data["attr_type"] = validated_data.get("attr_type", None)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        # validated_data["attr_type"] = validated_data.get("attr_type_id", None)
        return super().create(validated_data)


class DatasetTemplateSerializer(serializers.ModelSerializer):
    """
    データセットテンプレートシリアライザー
    """

    created_by = UserSerializer(read_only=True)
    attrs = DatasetTemplateAttrSerializer(source="attr_set", many=True)
    source_dataset = DatasetSerializer(read_only=True)

    class Meta:
        model = DatasetTemplate
        fields = [
            "id",
            "name",
            "desc",
            "attrs",
            "source_dataset",
            "created_at",
            "updated_at",
            "created_by",
        ]

    def get_fields(self, *args, **kwargs):
        fields = super(DatasetTemplateSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get("request", None)
        if request and getattr(request, "method", None) == "PUT":
            fields["name"].required = False
            fields["desc"].required = False
            fields["attrs"].required = False
        return fields


class DatasetTemplateApplyJobSerializer(serializers.Serializer):
    """"""

    dataset_id = serializers.CharField()  # TODO: validate dataset
    attr_set = serializers.DictField()  # TODO: validate dataset
    output_name = serializers.CharField()

    task_id = serializers.CharField(read_only=True)
    result = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    has_error = serializers.BooleanField(read_only=True)
    errors = serializers.DictField(child=serializers.CharField(), read_only=True)
    error_messages = serializers.ListField(child=serializers.CharField(), read_only=True)


class DatasetTemplatePreviewSerializer(serializers.Serializer):
    """"""

    dataset_id = serializers.CharField()  # TODO: validate dataset
    attr_set = serializers.DictField()  # TODO: validate dataset
    output_name = serializers.CharField()

    task_id = serializers.CharField(read_only=True)
    result = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    has_error = serializers.BooleanField(read_only=True)
    errors = serializers.DictField(child=serializers.CharField(), read_only=True)
    error_messages = serializers.ListField(child=serializers.CharField(), read_only=True)
