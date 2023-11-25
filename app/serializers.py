# serializers.py
from rest_framework import serializers
from .models import *
from account.models import Account

        
# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = account
#         fields = ['id', 'name', 'password']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'creator', 'amount_of_users', 'song', 'timer']
