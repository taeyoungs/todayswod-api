from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MembershipSerializer
from .models import Membership


@api_view(["GET"])
def get_memberships(request):

    if request.method == "GET":
        memberships = Membership.objects.all()
        serialized_memberships = MembershipSerializer(memberships, many=True).data
        return Response(serialized_memberships, status=status.HTTP_200_OK)