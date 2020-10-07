from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        exclude = ()
        read_only_fields = (
            "id",
            "created",
            "updated",
            "box",
        )