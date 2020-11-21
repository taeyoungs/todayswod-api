from rest_framework import serializers
from boxes.serializers import BoxSerializer
from .models import Wod, WodSort


class WodSortSerializer(serializers.ModelSerializer):
    class Meta:
        model = WodSort
        fields = ("name",)


class WodExistSerializer(serializers.ModelSerializer):
    title = WodSortSerializer()

    class Meta:
        model = Wod
        fields = (
            "id",
            "date",
            "title",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
        )


class WodSerializer(serializers.ModelSerializer):

    box = BoxSerializer(read_only=True)
    title = WodSortSerializer()

    class Meta:
        model = Wod
        read_only_fields = (
            "id",
            "created",
            "updated",
        )
        fields = (
            "id",
            "title",
            "content",
            "comment",
            "time",
            "rounds",
            "rest_sec",
            "round_sec",
            "box",
            "date",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        wod = Wod.objects.create(**validated_data, box=request.user.box)

        return wod
