from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Wod
from .serializers import WodSerializer


@api_view(["GET"])
def get_wods(request):

    if request.method == "GET":
        wods = Wod.objects.all()
        serialized_wods = WodSerializer(wods, many=True).data
        return Response(serialized_wods, status=status.HTTP_200_OK)
