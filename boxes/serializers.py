from rest_framework import serializers
from .models import Box


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = (
            "name",
            "address",
            "certification_code",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
        )