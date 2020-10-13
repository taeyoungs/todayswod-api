from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import MembershipSerializer
from .models import Membership
from wods.permissions import IsBoxOwner


class MembershipViewSet(ModelViewSet):

    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        now = timezone.now()
        instance = self.get_object()
        if instance.end_term < now.date():
            instance.state = Membership.STATE_EXPIRED
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)