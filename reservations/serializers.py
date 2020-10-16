from django.utils import timezone
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
        try:
            user_membership = Membership.objects.get(user=request.user)
            # 홀딩, 만료 체크
            if (
                user_membership.state == Membership.STATE_HOLDING
                or user_membership.state == Membership.STATE_EXPIRED
            ):
                raise serializers.ValidationError("홀딩 또는 만료 상태")

            # 회원권 종류에 따른 예약 가능 여부 체크
            now = timezone.now()
            if user_membership.title == "term":
                if (
                    user_membership.start_term > now.date()
                    and user_membership.end_term < now.date()
                ):
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
            except Schedule.DoesNotExist:
                raise serializers.ValidationError("박스 스케줄 정보 없음")
        except Membership.DoesNotExist:
            raise serializers.ValidationError("회원권 정보 없음")
