from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from .permissions import IsOwner
from .serializers import BoxSerializer
from .models import Box
from users.models import User


class BoxViewSet(ModelViewSet):

    queryset = Box.objects.all()
    serializer_class = BoxSerializer

    def get_permissions(self):

        if self.action == "partial_update" or self.action == "coach":
            permission_classes = [IsOwner]
        elif self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["get"], url_path="coach/(?P<coach_pk>[^/.]+)")
    def coach(self, request, pk, coach_pk):
        if coach_pk is not None:
            box = self.get_object()
            try:
                coach = User.objects.get(pk=coach_pk)
                coaches = box.coach.all()
                if coach in coaches:
                    box.coach.remove(coach)
                else:
                    box.coach.add(coach)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)