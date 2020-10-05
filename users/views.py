from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User


@api_view(["GET"])
def get_users(request):

    if request.method == "GET":
        users = User.objects.all()
        serialized_users = UserSerializer(users, many=True).data
        return Response(data=serialized_users, status=status.HTTP_200_OK)
