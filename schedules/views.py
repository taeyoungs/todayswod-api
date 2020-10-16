from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import ScheduleSerializer
from .models import Schedule
from wods.permissions import IsBoxOwner


class ScheduleViewSet(ModelViewSet):

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        elif (
            self.action == "destroy"
            or self.action == "partial_update"
            or self.action == "update"
            or self.action == "create"
        ):
            permission_classes = [IsBoxOwner]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    # Override로 날짜 정보 넘겨주기
    def list(self, request, *args, **kwargs):
        date = request.GET.get("date", None)
        if date is not None:
            schedules = Schedule.objects.filter(box=request.user.box)
            queryset = self.filter_queryset(schedules)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            # 예약 인원 표시하는 필드를 위한 date 정보
            serializer = self.get_serializer(
                queryset, many=True, context={"date": date}
            )
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
