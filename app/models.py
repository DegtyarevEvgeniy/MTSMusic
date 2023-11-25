from django.db import models
import uuid
from django.forms import ModelForm
from datetime import datetime
from account.models import *
from jsonfield import JSONField



class Room(models.Model):
    name = models.CharField(max_length=255)
    # creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount_of_users = models.IntegerField()
    song = models.CharField(max_length=255)
    timer = models.IntegerField()

    def __str__(self):
        return self.name
    

class Song(models.Model):
    name = models.CharField(max_length=255)
    length = models.IntegerField()

    def __str__(self):
        return self.name