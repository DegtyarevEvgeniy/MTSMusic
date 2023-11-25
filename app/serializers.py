# serializers.py
from rest_framework import serializers
from .models import *
from account.models import Account

        
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [  'id',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'phone',
                    'city',
                    'userImage',
                    'is_admin',
                    'is_superuser',
                    'is_staff',
                    'is_active',
                    'payment_account',
                    'confirmed',
                    'room',
                    ]

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'creator', 'amount_of_users', 'song', 'timer']
        
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'name', 'length']

