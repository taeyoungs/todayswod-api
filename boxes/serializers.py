from rest_framework import serializers
from .models import Box
from users.serializers import UserSerializer


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = (
            "id",
            "name",
            "address",
            "owner",
            "coach",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
            "certification_code",
        )