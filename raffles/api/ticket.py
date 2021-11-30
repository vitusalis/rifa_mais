from raffles.models import Ticket
from rest_framework import serializers, viewsets
from rest_framework.response import Response


class TicketSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="_id", read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "raffle", "name", "cpfCnpj", "ticket_number", "status"]
        read_only_fields = (
            "status",
            "id",
            "_id",
        )
        extra_kwargs = {
            'raffle': {'required': True},
            'ticket_number': {'required': True},
            'name': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
        }


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        raffle_id = self.request.query_params.get("raffle", None)
        email = self.request.query_params.get("email", None)

        if raffle_id:
            queryset = queryset.filter(raffle_id=raffle_id).order_by("ticket_number")
        if email:
            queryset = queryset.filter(email=email)
        result = TicketSerializer(queryset, many=True, context={"request": request})
        return Response(result.data)

    def create(self, request, *args, **kwargs):
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance
        
        try:
            response = instance.create_payment()
        except Exception as e:
            instance.delete()
            return Response({"error": str(e)}, status=400)
        
        if response.get("type") == "error":
            return Response(response, status=400)

        data = {**serializer.data, "payment_link": response.get("payment_link")}
        return Response(data, status=201)

    def retrieve(self, request, *args, **kwargs):
        return Response({}, status=403)

    def update(self, request, *args, **kwargs):
        return Response({}, status=403)

    def partial_update(self, request, *args, **kwargs):
        return Response({}, status=403)

    def destroy(self, request, *args, **kwargs):
        return Response({}, status=403)
