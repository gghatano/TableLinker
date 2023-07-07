from rest_framework import serializers

from datasets.models import Dataset, DatasetGroup, DatasetSource
from users.serializers import UserSerializer

from ..validators.file_format import FileFormatValidator
from .dataset_annotate_serializer import DatasetAnnotateSerializer
from .dataset_attr_serializer import DatasetAttrSerializer
from .dataset_source_serializer import DatasetSourceSerializer


class DatasetGroupSerializer(serializers.ModelSerializer):
    """
    データセットグループシリアライザー
    """

    created_by = UserSerializer(read_only=True)
    source = DatasetSourceSerializer(required=False)
    name = serializers.CharField(required=True)
    # original_file = serializers.FileField(required=True, validators=[FileFormatValidator()])
    original_file = serializers.FileField(required=False, validators=[FileFormatValidator()])

    class Meta:
        model = Dataset
        fields = [
            "id",
            "name",
            "original_file",
            "created_at",
            "updated_at",
            "created_by",
            "source",
        ]

    def get_fields(self, *args, **kwargs):
        fields = super(DatasetGroupSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get("request", None)
        if request and getattr(request, "method", None) == "PUT":
            fields["original_file"].required = False
        return fields

    def create(self, validated_data):
        source_data = None
        try:
            source_data = validated_data.pop("source")
        except KeyError:
            pass

        dataset_group = DatasetGroup(**validated_data)
        dataset_group.created_by = self.context["request"].user
        dataset_group.current_version = self.context["current_version"]
        dataset_group.save()

        if source_data is not None:
            DatasetSource.objects.create(dataset_group=dataset_group, **source_data)

        return dataset_group

    def update(self, instance, validated_data):
        source_data = None
        try:
            source_data = validated_data.pop("source")
        except KeyError:
            pass

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if source_data is not None:
            source_instance = instance.source
            for attr, value in source_data.items():
                setattr(source_instance, attr, value)
            source_instance.save()

        return instance


class DatasetSerializer(serializers.ModelSerializer):
    """
    データセットシリアライザー
    """

    created_by = UserSerializer(read_only=True)
    stared = serializers.SerializerMethodField(read_only=True)
    attrs = DatasetAttrSerializer(source="attr_set", many=True, read_only=True)
    annotates = DatasetAnnotateSerializer(source="annotate_set", many=True, read_only=True)
    source = DatasetSourceSerializer(required=False)
    public_level_name = serializers.CharField(read_only=True)

    class Meta:
        model = Dataset
        fields = [
            "id",
            "num_records",
            "num_columns",
            "file_size",
            "attr_names",
            "status",
            "data_file_url",
            "analyzed_at",
            "is_analyzed",
            "public_level_name",
            "encoding",
            "created_at",
            "updated_at",
            "created_by",
            "data_file",
            "source",
            "attrs",
            "annotates",
            "has_annotates",
            "stared",
        ]

    def get_fields(self, *args, **kwargs):
        fields = super(DatasetSerializer, self).get_fields(*args, **kwargs)
        return fields

    def create(self, validated_data):
        dataset = Dataset(**validated_data)
        dataset.created_by = self.context["request"].user
        dataset.current_version = self.context["current_version"]
        dataset.dataset_group = self.context["dataset_group"]
        dataset.save()
        return dataset

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def get_stared(self, instance):
        if "request" in self.context:
            user = self.context["request"].user
            return instance.stared_users.filter(pk=user.id).exists()
        else:
            return None


class DatasetUpdateSerializer(DatasetSerializer):
    field = serializers.CharField(max_length=100, required=False)
