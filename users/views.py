import jwt
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
from boxes.models import Box
from alerts.permissions import IsBoxOwnerOrAdmin


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsBoxOwnerOrAdmin]
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

    def list(self, request, *args, **kwargs):

        # 박스 주인일 경우
        if request.user == request.user.box.owner:
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
            user = authenticate(username=username, password=password)
            if user is not None:
                encoded_jwt = jwt.encode(
                    {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
                )
                return Response(data={"token": encoded_jwt, "pk": user.pk})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
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
                    return Response(status=status.HTTP_200_OK)
            except Box.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)