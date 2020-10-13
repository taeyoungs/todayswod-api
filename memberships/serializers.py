from rest_framework import serializers
from .models import Membership
from users.models import User


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = (
            "id",
            "title",
            "state",
            "cnt",
            "start_term",
            "end_term",
            "user",
        )
        read_only_fields = (
            "id",
            "updated",
            "created",
            "user",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        user_pk = request.data.get("user_pk")
        user = User.objects.get(pk=user_pk)
        membership = Membership.objects.create(**validated_data, user=user)
        return membership
