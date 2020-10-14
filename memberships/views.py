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
from wods.permissions import IsBoxOwner


class MembershipViewSet(ModelViewSet):

    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        # ToDo: 3일전 or 3개 남았을 때 알림을 생성
        # ToDo: 횟수랑 기간이랑 구별
        now = timezone.now()
        instance = self.get_object()
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
        if instance.end_term < now.date():
            instance.state = Membership.STATE_EXPIRED
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)