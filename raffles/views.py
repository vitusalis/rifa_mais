from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from raffles.models import Raffle, Ticket
from raffles.serializers import RaffleSerializer, TicketSerializer
from raffles.serializers import UserSerializer


class AuthenticatedOrPostOnly(permissions.BasePermission):
    message = "Only authenticated users may put or delete"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return True
        return False


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "raffles": reverse("raffle-list", request=request, format=format),
            "tickets": reverse("ticket-list", request=request, format=format),
        }
    )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RaffleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [AuthenticatedOrPostOnly]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        raffle_id = self.request.query_params.get("raffle", None)
        if raffle_id:
            return Ticket.objects.filter(raffle_id=raffle_id).order_by("ticket_number")
        return Ticket.objects.all()

    def list(self, request, *args, **kwargs):
        result = TicketSerializer(self.get_queryset(), many=True, context={"request": request})
        return Response(result.data)

    def update(self, request, *args, **kwargs):
        return Response({}, status=403)

    def partial_update(self, request, *args, **kwargs):
        return Response({}, status=403)

    def destroy(self, request, *args, **kwargs):
        return Response({}, status=403)
