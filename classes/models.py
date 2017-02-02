import uuid
from .signals import *

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save

default_slug = 'Hello'


class MyUser(AbstractUser):
    owner = models.IntegerField(null=True)
    department = models.CharField(max_length=200, help_text="Required. Max 200 characters for department name.")
    employee_number = models.CharField(max_length=100, help_text="Required. Max 100 characters for employee number.")
    employee_designation = models.CharField(max_length=300, help_text="Required.  Max"
                                                                      " 300 characters for employee number.")
    # REQUIRED_FIELDS = ['owner']


class BoardCategory(models.Model):
    """
    Manage Category Of avail.. Boards.
    """
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = "Board Categories"

    def __str__(self):
        """Return course title and first 8 char"""
        return self.title


class ClassCategory(models.Model):
    """
    Manage Category Of classes.
    """
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(editable=False)
    board = models.ForeignKey(BoardCategory)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = "Grades"
        verbose_name = "Grade"

    def __str__(self):
        """Return course title and first 8 char"""
        return self.title


pre_save.connect(pre_save_create_slug, sender=ClassCategory)
