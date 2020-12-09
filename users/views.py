import jwt
import requests
import os
from random import randrange
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import UserSerializer
from .permissions import IsSelf
from .models import User
from reservations.models import Reservation
from boxes.models import Box
from boxes.serializers import BoxSerializer
from memberships.models import Membership
from alerts.permissions import IsBoxOwnerOrAdmin


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif (
            self.action == "retrieve"
            or self.action == "create"
            or self.action == "token"
        ):
            permission_classes = [AllowAny]
        elif self.action == "box_authentication":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        try:
            user = User.objects.get(email=email)
            return Response(status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

    def list(self, request, *args, **kwargs):

        # 박스 주인일 경우
        if request.user == request.user.box.owner:
            # if False:
            users = User.objects.filter(box=request.user.box)
            queryset = self.filter_queryset(users)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # Admin일 경우
        else:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def token(self, request):

        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if username is not None and password is not None:
            try:
                u = User.objects.get(username=username)
                user = authenticate(username=username, password=password)
                if user is not None:
                    encoded_jwt = jwt.encode(
                        {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
                    )
                    serialized_user = self.get_serializer(user).data
                    return Response(
                        data={
                            "token": encoded_jwt,
                            "userId": user.pk,
                            "user": serialized_user,
                        }
                    )
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def box_authentication(self, request):

        certification_code = request.data.get("certification_code", None)

        if certification_code is not None:
            try:
                box = Box.objects.get(certification_code=certification_code)
                if box is not None:
                    user = request.user
                    user.box = box
                    user.save()
                    m = Membership.objects.filter(user__box=box, user=user)
                    print(m)
                    if m.count == 0:
                        # 등록한 박스에 회원권이 존재하지 않는 경우
                        user.registration_state = User.STATE_PENDING
                    else:
                        user.registration_state = User.STATE_REGISTERED
                    user.save()
                    serialized_box = BoxSerializer(box).data
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            "box": serialized_box,
                            "registrationState": user.registration_state,
                        },
                    )
            except Box.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def enrollment(self, request, pk):
        action = request.GET.get("action", None)
        user = self.get_object()
        # action: confirm / cancel

        if action is not None and user is not None:
            if action == "confirm":
                user.registration_state = User.STATE_REGISTERED
                user.save()
            elif action == "cancel":
                user.registration_state = User.STATE_UNREGISTERED
                user.box = None
                user.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def pw_reset(self, request):
        email = request.data.get("email", None)
        certification_number = randrange(100000, 1000000)
        if email is not None:
            try:
                user = User.objects.get(username=email)
                user.certification_number = certification_number
                user.save()
                # results = requests.post(
                #     "https://api.mailgun.net/v3/sandbox84ef292259734d5baaa226547f1981b4.mailgun.org/messages",
                #     auth=("api", os.environ.get("MAILGUN_API_KEY")),
                #     data={
                #         "from": "오늘의 와드 <mailgun@sandbox84ef292259734d5baaa226547f1981b4.mailgun.org>",
                #         "to": [
                #             email,
                #         ],
                #         "subject": "비밀번호 재설정 인증번호",
                #         "text": f"인증번호: {certification_number}",
                #     },
                # )
                # print(results)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def certification(self, request):
        certification_number = request.data.get("certification_number", None)
        email = request.data.get("email", None)

        print(certification_number, email)

        if certification_number is not None and email is not None:
            user = User.objects.get(username=email)
            if user.certification_number != int(certification_number):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                # user.certification_number = None
                # user.save()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def pw_set(self, request):
        email = request.data.get("email", None)
        pw = request.data.get("pw", None)

        if email is not None and pw is not None:
            try:
                user = User.objects.get(username=email)
                user.set_password(pw)
                user.save()
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def revoke(self, request, pk):
        user = self.get_object()
        now = timezone.now()
        if user is not None:
            Reservation.objects.filter(date__gte=now.date(), user=user).delete()
            user.box = None
            user.registration_state = User.STATE_UNREGISTERED
            user.save()
            serialized_user = self.get_serializer(user).data

            # ToDo: Box 변경에 따른 Alerts 삭제
            return Response(status=status.HTTP_200_OK, data=serialized_user)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)