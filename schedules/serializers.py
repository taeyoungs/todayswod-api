from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):

    coach = UserSerializer()

    class Meta:
        model = Schedule
        fields = (
            "id",
            "time",
            "user_limit",
            "box",
            "coach",
        )
        read_only_fields = (
            "id",
            "updated",
            "created",
            "box",
        )