from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    owner = models.IntegerField(null=True)
    # REQUIRED_FIELDS = ['owner']


class ClassCategory(models.Model):
    """
    Manage Category Of classes.
    """
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Return course title and first 8 char"""
        return self.title


# Create your models here.
