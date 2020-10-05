from rest_framework import serializers
from .models import Membership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        exclude = ("modified",)
        read_only_fields = (
            "id",
            "updated",
            "created",
            "user",
        )