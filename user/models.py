from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    GENDER_OPTION = (
        (1, "male"),
        (2, "female")
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    mobile = models.CharField(max_length=15, null=True)
    gender = models.IntegerField(choices=GENDER_OPTION, null=True)

    def __str__(self):
        return self.name
