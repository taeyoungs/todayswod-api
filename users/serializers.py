from rest_framework import serializers
from .models import User
from boxes.serializers import BoxSerializer


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "last_name",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
        )


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    box = BoxSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "gender",
            "has_new_alert",
            "box",
            "registration_state",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
            "box",
            "has_new_alert",
            "registration_state",
        )

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
