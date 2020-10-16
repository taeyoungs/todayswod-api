from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Alert
from .serializers import AlertSerializer
from .permissions import IsBoxOwnerOrAdmin
from users.models import User


class AlertViewSet(ModelViewSet):

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsBoxOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):

        # 박스 주인은 자신에 대한 알림이 존재할까?

        # 사용자 전용 알림과 사용자가 속한 박스 알림만 QuerySet으로
        user_alerts = Alert.objects.filter(user=request.user)
        box_alerts = Alert.objects.filter(box=request.user.box)
        alerts = user_alerts.union(box_alerts).order_by("-updated")

        queryset = self.filter_queryset(alerts)

        # 알림 확인
        request.user.has_new_alert = False
        request.user.save()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        # 회원권 만료 알림은 Membership 쪽에서 생성할 것이니 여기선 BoxOwner만
        # 여기서 알림을 생성할 수 있는 사람은 Box 주인뿐 (permission)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 해당 박스 소속인 사용자들에게 새로운 알림이 있다고 표시
        User.objects.filter(box=request.user.box).update(has_new_alert=True)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
