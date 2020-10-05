from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BoxSerializer
from .models import Box


@api_view(["GET"])
def get_boxes(request):

    if request.method == "GET":
        boxes = Box.objects.all()
        serialized_boxes = BoxSerializer(boxes, many=True).data
        return Response(serialized_boxes, status=status.HTTP_200_OK)
