# serializers.py
from rest_framework import serializers
from .models import *


class BetaServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetaServer
        fields = ['time']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'password']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'creator', 'amount_of_users', 'song', 'timer']
