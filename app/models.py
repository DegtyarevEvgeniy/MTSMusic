from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_of_users = models.IntegerField()
    song = models.CharField(max_length=255)
    timer = models.IntegerField()

    def __str__(self):
        return self.name

class BetaServer(models.Model):
    time = models.IntegerField()