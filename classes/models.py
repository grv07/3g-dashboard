import uuid
from .signals import *

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save

default_slug = 'Hello'


class MyUser(AbstractUser):
    owner = models.IntegerField(null=True)
    # REQUIRED_FIELDS = ['owner']


class ClassCategory(models.Model):
    """
    Manage Category Of classes.
    """
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(editable=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Return course title and first 8 char"""
        return self.title


pre_save.connect(pre_save_create_slug, sender=ClassCategory)
