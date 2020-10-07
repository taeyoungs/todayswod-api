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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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

        certification_code = request.data("certification_code", None)
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


# class MyView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         serialized_user = ReadUserSerializer(user).data
#         return Response(serialized_user, status=status.HTTP_200_OK)


# @api_view(["GET", "POST"])
# def get_users(request):

#     if request.method == "GET":
#         users = User.objects.all()
#         serialized_users = ReadUserSerializer(users, many=True).data
#         return Response(data=serialized_users, status=status.HTTP_200_OK)
#     elif request.method == "POST":
#         serializer = WriteUserSerializer(data=request.data)
#         print(request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             print(user)
#             return Response()
