from raffles.models import Raffle
from rest_framework import permissions, serializers, viewsets


class RaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raffle
        fields = "__all__"


class RaffleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
    permission_classes = [permissions.AllowAny]
