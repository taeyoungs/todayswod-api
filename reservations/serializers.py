from rest_framework import serializers
from .models import Reservation
from schedules.models import Schedule
from schedules.serializers import ScheduleSerializer
from memberships.models import Membership


class ReservationSerializer(serializers.ModelSerializer):

    schedule = ScheduleSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "date",
            "state",
            "schedule",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
            "user",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        schedule_pk = request.data.get("schedule_pk")
        date = request.data.get("date")
        user_membership = Membership.objects.get(user=request.user)
        schedule = Schedule.objects.get(pk=schedule_pk)
        reservations_count = schedule.reservations.filter(date=date).count()
        if reservations_count < schedule.user_limit:
            reservation = Reservation.objects.create(
                **validated_data, user=request.user, schedule=schedule
            )
            # 횟수제 회원권 체크 및 만료 처리
            if (
                user_membership.title == "count"
                and user_membership.state != Membership.STATE_EXPIRED
            ):
                if user_membership.cnt - 1 == 0:
                    user_membership.state = Membership.STATE_EXPIRED
                user_membership.cnt -= 1
                user_membership.save()
            return reservation
        else:
            raise serializers.ValidationError("예약 제한 인원 초과")
