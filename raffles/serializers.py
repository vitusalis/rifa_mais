from django.contrib.auth.models import User, Group
from raffles.models import Ticket, Raffle
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["_id", "raffle", "name", "email", "phone", "ticket_number", "status", "instagram"]


class RaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raffle
        fields = ["id", "_id", "name", "ticket_amount", "ticket_price", "date", "cover", "photo_1", "photo_2",
                  "photo_3", "photo_4", "info", "status"]
