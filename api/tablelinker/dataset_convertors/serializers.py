from rest_framework import serializers

from datasets.models import Dataset, DatasetAttr


class ParamSerializer(serializers.Serializer):
    """
    パラメータシリアライザー
    """

    name = serializers.CharField()
    description = serializers.CharField()
    help_text = serializers.CharField()
    group = serializers.CharField()
    default_value = serializers.CharField()
    label = serializers.CharField()
    label = serializers.CharField()
    required = serializers.BooleanField()
    type = serializers.CharField()
    arguments = serializers.DictField(child=serializers.CharField(), read_only=True)


class FilterSerializer(serializers.Serializer):
    """
    フィルターシリアライザー
    """

    key = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    help_text = serializers.CharField()
    params = ParamSerializer(many=True)

    stared = serializers.SerializerMethodField()

    def get_stared(self, instance):
        stared_filter_keys = self.context["stared_filter_keys"]
        if stared_filter_keys is None:
            return False
        return instance.key in stared_filter_keys


class DatasetPreviewSerializer(serializers.Serializer):

    dataset_id = serializers.CharField()  # TODO: validate dataset
    filter_key = serializers.CharField()  # TODO: validate filter_key

    task_id = serializers.CharField(read_only=True)
    result = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    has_error = serializers.BooleanField(read_only=True)
    errors = serializers.DictField(child=serializers.CharField(), read_only=True)
    error_messages = serializers.ListField(child=serializers.CharField(), read_only=True)


class DatasetConvertJobSerializer(serializers.Serializer):

    dataset_id = serializers.CharField()  # TODO: validate dataset
    filter_key = serializers.CharField()  # TODO: validate filter_key
    output_name = serializers.CharField()

    task_id = serializers.CharField(read_only=True)
    result = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    has_error = serializers.BooleanField(read_only=True)
    errors = serializers.DictField(child=serializers.CharField(), read_only=True)
    error_messages = serializers.ListField(child=serializers.CharField(), read_only=True)


class DatasetSerializer(serializers.ModelSerializer):
    """
    データセットシリアライザー
    """

    stared = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = [
            "id",
            "num_records",
            "num_columns",
            "file_size",
            "attr_names",
            "data_file",
            "analyzed_at",
            "public_level",
            "encoding",
            "created_at",
            "updated_at",
            "created_by",
            "stared",
        ]

    def get_stared(self, instance):
        user = self.context["request"].user
        return instance.stared_users.filter(pk=user.id).exists()


class DatasetAttrSerializer(serializers.ModelSerializer):
    """
    データセット属性シリアライザー
    """

    class Meta:
        model = DatasetAttr
        fields = "__all__"
