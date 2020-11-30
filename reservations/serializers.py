from datetime import date
from django.utils import timezone
from rest_framework import serializers
from schedules.models import Schedule
from schedules.serializers import ScheduleSerializer
from users.serializers import UserSerializer
from memberships.models import Membership
from schedules.models import Schedule
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    schedule = ScheduleSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "date",
            "state",
            "user",
            "schedule",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
            "user",
            "schedule",
        )

    def validate(self, data):

        print(data)
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        schedule_pk = request.data.get("schedule_id")
        # 예약하려는 날짜 정보
        dateStr = request.data.get("date")
        year, month, day = list(map(int, dateStr.split("-")))
        try:
            user_membership = Membership.objects.get(user=request.user)
            # 홀딩, 만료 체크
            if (
                user_membership.state == Membership.STATE_HOLDING
                or user_membership.state == Membership.STATE_EXPIRED
            ):
                raise serializers.ValidationError("홀딩 또는 만료 상태")

            # 회원권 종류에 따른 예약 가능 여부 체크
            # now = timezone.now()
            if user_membership.title == "term":
                if user_membership.start_term > date(
                    year, month, day
                ) and user_membership.end_term < date(year, month, day):
                    raise serializers.ValidationError("회원권 갱신 필요")
            else:
                if user_membership.cnt <= 0:
                    raise serializers.ValidationError("회원권 갱신 필요")
            try:
                schedule = Schedule.objects.get(pk=schedule_pk)

                # 자신의 박스 스케줄을 조회했는지 체크
                if request.user.box != schedule.box:
                    raise serializers.ValidationError("타 박스 스케줄 조회")

                # 예약 제한 인원 체크
                reservations_count = schedule.reservations.filter(date=dateStr).count()
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
                    print(reservation)
                    return reservation
                else:
                    raise serializers.ValidationError("예약 제한 인원 초과")
            except Schedule.DoesNotExist:
                raise serializers.ValidationError("박스 스케줄 정보 없음")
        except Membership.DoesNotExist:
            raise serializers.ValidationError("회원권 정보 없음")

    def update(self, instance, validated_data):
        request = self.context.get("request")
        schdule_id = request.data.get("schedule_id")
        schedule = Schedule.objects.get(id=schdule_id)
        instance.date = validated_data.get("date", instance.date)
        instance.user = validated_data.get("user", instance.user)
        instance.state = validated_data.get("state", instance.state)
        instance.schedule = schedule
        instance.save()
        return instance
