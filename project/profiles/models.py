from django.contrib.auth.models import User
from django.db import models


class Settings(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.key


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)


    def __str__(self):
        return self.full_name