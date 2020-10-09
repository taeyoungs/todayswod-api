from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):

    reservations_count = serializers.SerializerMethodField(
        method_name="get_reservations_count"
    )

    def get_reservations_count(self, obj):
        date = self.context.get("date")
        reservations_count = obj.reservations.filter(date=date).count()
        return reservations_count

    class Meta:
        model = Schedule
        fields = (
            "id",
            "start_time",
            "end_time",
            "user_limit",
            "box",
            "coach",
            "reservations_count",
        )
        read_only_fields = (
            "id",
            "updated",
            "created",
            "box",
        )

    def validate(self, data):
        request = self.context.get("request")
        if request.method == "POST":
            if self.instance:
                start_time = data.get("start_time", self.instance.start_time)
                end_time = data.get("end_tiem", self.instance.end_time)
            else:
                start_time = data.get("start_time")
                end_time = data.get("end_time")

            if start_time >= end_time:
                raise serializers.ValidationError(
                    "End time must be set greater than start time"
                )
            else:
                filter_kwargs = {}
                filter_kwargs["start_time__gte"] = start_time
                filter_kwargs["end_time__lte"] = end_time
                schedules_count = request.user.box.schedules.filter(
                    **filter_kwargs
                ).count()
                if schedules_count != 0:
                    raise serializers.ValidationError("Schedule already exists")
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        schedule = Schedule.objects.create(**validated_data, box=request.user.box)

        return schedule