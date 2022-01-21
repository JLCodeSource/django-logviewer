from rest_framework import serializers
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)
from logviewer.models import (
    Asset,
    Log,
)


class AssetSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "name", "type", "IP", "site", "phase", "username", "password"]
        list_serializer_class = BulkListSerializer


class LogSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = [
            "id",
            "asset",
            "seqnumber",
            "message_id",
            "agent_id",
            "category",
            "severity",
            "timestamp",
            "message",
            "raw_data",
            "fqdd",
            "resolved",
        ]
        list_serializer_class = BulkListSerializer
