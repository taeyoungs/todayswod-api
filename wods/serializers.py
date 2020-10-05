from rest_framework import serializers
from boxes.serializers import BoxSerializer
from .models import Wod


class WodSerializer(serializers.ModelSerializer):

    box = BoxSerializer(read_only=True)

    class Meta:
        model = Wod
        read_only_fields = (
            "id",
            "created",
            "updated",
        )
        fields = (
            "title",
            "content",
            "comment",
            "time",
            "rounds",
            "rest_sec",
            "round_sec",
            "box",
        )
