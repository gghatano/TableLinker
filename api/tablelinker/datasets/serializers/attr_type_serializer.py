from rest_framework import serializers


class AttrTypeSerializer(serializers.Serializer):
    """
    属性型シリアライザー
    """

    name = serializers.CharField(required=True)
    value = serializers.CharField(required=True)
