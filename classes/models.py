from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    owner = models.IntegerField(null=True)
    department = models.CharField(max_length=200, help_text="Required. Max 200 characters for department name.")
    employee_number = models.CharField(max_length=100, help_text="Required. Max 100 characters for employee number.")
    employee_designation = models.CharField(max_length=300, help_text="Required.  Max"
                                                                      " 300 characters for employee number.")
    type = models.CharField(choices=[('DEFAULT', 'default',), ('STUDENT', 'student',), ('TEACHER', 'teacher',),
                                     ('UPLOADER', 'uploader'), ('ADMIN', 'admin',),
                                     ('SUPER-ADMIN', 'super-admin')], max_length=20, default='DEFAULT')
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
    board = models.ForeignKey(BoardCategory)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = "Grades"
        verbose_name = "Grade"

    def __str__(self):
        """Return course title and first 8 char"""
        return self.title

# Create your models here.
