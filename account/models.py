from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=13)
    profile = models.ImageField(blank=True, null=True)


class Board(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
