from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    image_profile = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='profile_images/default.png')
    bio = models.TextField(blank=True, null=True, default='')
    
    def __str__(self):
        return self.username
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)