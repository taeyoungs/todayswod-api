from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Wod
from .serializers import WodSerializer
from .permissions import IsBoxOwner


class WodViewSet(ModelViewSet):

    queryset = Wod.objects.all()
    serializer_class = WodSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsBoxOwner]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # 1. 하루에 1개의 예약만 가능하게끔 - V
        # 2. 예약 인원 넘는 요청 불가하게 - V
        date = request.data.get("date", None)
        if date is not None:
            try:
                request.user.box.wods.get(date=date)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Wod.DoesNotExist:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid()
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)