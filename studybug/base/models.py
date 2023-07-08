from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    # participants =

    updated = models.DateTimeField(
        auto_now=True
    )  # auto_now changes the value every time it changes
    created = models.DateTimeField(
        auto_now_add=True
    )  # auto_now_add only alters it the fist time it is updated - that is when it is created

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
