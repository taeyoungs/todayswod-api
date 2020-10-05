from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "last_name",
            "is_owner",
            "box",
            "gender",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
        )