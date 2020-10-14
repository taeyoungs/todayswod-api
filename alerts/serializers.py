from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = (
            "id",
            "updated",
            "alert_type",
            "title",
            "content",
            "user",
            "box",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
            "user",
            "box",
        )

    def create(self, validated_data):

        request = self.context.get("request")
        alert = Alert.objects.create(**validated_data, box=request.user.box)
        return alert