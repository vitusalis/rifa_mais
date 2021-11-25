from raffles.models import Ticket
from rest_framework import serializers, viewsets
from rest_framework.response import Response


class TicketSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)
    class Meta:
        model = Ticket
        fields = ["id", "raffle", "name", "ticket_number", "status"]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.all()

        raffle_id = self.request.query_params.get("raffle", None)
        email = self.request.query_params.get("email", None)

        if raffle_id:
            queryset = queryset.filter(raffle_id=raffle_id).order_by("ticket_number")
        if email:
            queryset = queryset.filter(email=email)
        return Ticket.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result = TicketSerializer(queryset, many=True, context={"request": request})
        return Response(result.data)

    def retrieve(self, request, *args, **kwargs):
        return Response({}, status=403)

    def update(self, request, *args, **kwargs):
        return Response({}, status=403)

    def partial_update(self, request, *args, **kwargs):
        return Response({}, status=403)

    def destroy(self, request, *args, **kwargs):
        return Response({}, status=403)
