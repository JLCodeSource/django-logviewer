from rest_framework import serializers
from logviewer.models import (
    Asset,
    Log,
)


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "name", "IP", "site", "type", "phase"]


class LogSerializer(serializers.ModelSerializer):
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
