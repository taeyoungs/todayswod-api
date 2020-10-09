from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .serializers import ReservationSerializer
from .models import Reservation
from .permissions import IsSelf
from wods.permissions import IsBoxOwner


class ReservationViewSet(ModelViewSet):

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        if (
            self.action == "list"
            or self.action == "retrieve"
            or self.action == "delete"
        ):
            permission_classes = [IsAdminUser, IsBoxOwner, IsSelf]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # 1. 하루에 1개의 예약만 가능하게끔 - V
        # 2. 예약 인원 넘는 요청 불가하게
        date = request.data.get("date", None)
        if date is not None:
            try:
                r = request.user.reservations.get(date=date)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Reservation.DoesNotExist:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid()
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)