from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
