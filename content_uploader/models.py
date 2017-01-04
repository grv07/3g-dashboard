from django.db import models
from django.contrib.auth.models import User


class Uploader(models.Model):
    owner = models.IntegerField()
    user = models.OneToOneField(User)
# Create your models here.
