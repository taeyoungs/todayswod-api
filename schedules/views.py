from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ScheduleSerializer
from .models import Schedule


@api_view(["GET"])
def get_schedules(request):

    if request.method == "GET":
        schedules = Schedule.objects.all()
        serialized_schedules = ScheduleSerializer(schedules, many=True).data
        return Response(serialized_schedules, status=status.HTTP_200_OK)
