from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils.extra_functions import sao_paulo_now
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    last_login = models.DateTimeField(default=sao_paulo_now, blank=True, null=True)
    image_profile = CloudinaryField('image', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, default="")

    def __str__(self):
        return self.username


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(
        "Room", on_delete=models.CASCADE, related_name="messages", null=True, blank=True
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name="rooms", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
