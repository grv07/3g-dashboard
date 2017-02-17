from django.db import models
import uuid
from utils import  name_definition


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
        return name_definition(self.title, self.board)

