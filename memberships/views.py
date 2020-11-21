import datetime
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import MembershipSerializer
from .models import Membership
from alerts.models import Alert
from users.models import User
from wods.permissions import IsBoxOwner
from reservations.permissions import IsSelfOrBoxOwnerOrAdminUser


class MembershipViewSet(ModelViewSet):

    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        elif self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        now = timezone.now()
        # instance = self.get_object()
        instance = Membership.objects.get(user=pk)

        # 원래 Push 알림으로 해야하는 부분
        """
        two_days_ago = instance.end_term - datetime.timedelta(days=2)
        # print(two_days_ago)
        if now.date() == two_days_ago:
            Alert.objects.create(
                alert_type=Alert.TYPE_MESSAGE,
                title="회원권 만료 기한",
                content="회원권 만료 2일전 입니다.",
                user=request.user,
            )
        """
        if instance.state == Membership.STATE_HOLDING:
            if instance.hold_date < now.date():
                instance.state = Membership.STATE_PROGRESS
                instance.hold_date = None
                instance.save()
        if instance.end_term < now.date():
            instance.state = Membership.STATE_EXPIRED
            instance.save()
            request.user.registration_state = User.STATE_UNREGISTERED
            request.user.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def hold(self, request, pk):
        term = request.GET.get("term", None)
        if term is not None:
            membership = self.get_object()
            if membership.title == "term":
                # ex. term: 1, 2, 3, 4 ... 주 단위로
                membership.state = Membership.STATE_HOLDING
                membership.hold_date = membership.start_term + datetime.timedelta(
                    days=6
                )
                membership.start_term += datetime.timedelta(days=int(term) * 7)
                membership.end_term += datetime.timedelta(days=int(term) * 7)
                membership.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data="기간제 회원권만 홀딩 가능"
                )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="홀딩 기간 필요")
