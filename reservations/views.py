from django.utils import timezone
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .serializers import ReservationSerializer
from .models import Reservation
from .permissions import IsSelf, IsSelfOrBoxOwnerOrAdminUser
from wods.models import Wod
from wods.permissions import IsBoxOwner


class ReservationViewSet(ModelViewSet):

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        if (
            self.action == "list"
            or self.action == "retrieve"
            or self.action == "destroy"
            or self.action == "expiration"
        ):
            permission_classes = [IsSelfOrBoxOwnerOrAdminUser]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # 1. 하루에 1개의 예약만 가능하게끔 - V
        # 2. 예약 인원 넘는 요청 불가하게 - V
        date = request.data.get("date", None)
        if date is not None:
            try:
                request.user.box.wods.get(date=date)
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
            except Wod.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def expiration(self, request):
        now = timezone.now()
        date = now.date()
        old_reservations = Reservation.objects.filter(
            date__lt=date, state=Reservation.STATE_PENDING
        ).update(state=Reservation.STATE_CANCELED)
        return Response(status=status.HTTP_200_OK)

    # 우선 Toggle 말고 출석 확인하는 것만
    @action(detail=True, methods=["get"])
    def confirm(self, request, pk):
        reservation = self.get_object()
        if reservation.state == Reservation.STATE_PENDING:
            reservation.state = Reservation.STATE_CONFIRMED
            reservation.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)