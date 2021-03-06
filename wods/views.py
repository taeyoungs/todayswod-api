from calendar import calendar, monthrange
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from .models import Wod
from .serializers import WodSerializer, WodExistSerializer
from .permissions import IsBoxOwner


class WodViewSet(ModelViewSet):

    queryset = Wod.objects.all()
    serializer_class = WodSerializer

    def get_permissions(self):

        if self.action == "list" or self.action == "retrieve" or self.action == "date":
            permission_classes = [AllowAny]
        elif (
            self.action == "create"
            or self.action == "destroy"
            or self.action == "partial_update"
        ):
            permission_classes = [IsBoxOwner]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):

        # 박스 주인일 경우 자신의 박스 와드 전체 목록 조회
        if request.user == request.user.box.owner:
            wods = Wod.objects.filter(box=request.user.box)
            queryset = self.filter_queryset(wods)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # 박스를 이용하는 사용자일 경우 앞 뒤로 일주일치 와드 조회
        else:
            period = request.GET.get("period", None)
            if period is None:
                now = timezone.now()
                start_date = now.date() - timedelta(days=7)
                end_date = now.date() + timedelta(days=7)
                wods = Wod.objects.filter(
                    date__gte=start_date, date__lte=end_date, box=request.user.box
                ).order_by("date")

                queryset = self.filter_queryset(wods)

                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(queryset, many=True)

                return Response(data=serializer.data)
            else:
                # now = timezone.now()
                # print(period)
                year, month = period.split("-")
                _, lastDay = monthrange(int(year), int(month))

                wods = Wod.objects.filter(
                    date__gte=f"{year}-{month}-1",
                    date__lte=f"{year}-{month}-{lastDay}",
                    box=request.user.box,
                ).order_by("date")

                queryset = self.filter_queryset(wods)

                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = WodExistSerializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = WodExistSerializer(queryset, many=True)

                return Response(data=serializer.data)

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

    @action(detail=False, methods=["get"])
    def date(self, request):
        search = request.GET.get("date", None)
        if search is not None:
            try:
                wod = Wod.objects.filter(date=search)
                queryset = self.filter_queryset(wod)
                serializer = self.get_serializer(queryset, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Wod.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
