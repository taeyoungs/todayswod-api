from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "state",
            "schedule",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
            "user",
        )