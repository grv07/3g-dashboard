from django.db import models
from django.utils import timezone

from content_uploader.models import Uploader, MyUser


status_fields = [('ASSIGN', 'assign'), ('COMPLETE', 'complete')]


class Task(models.Model):
    """
    Task model for assigning task to the content uploader.kkk
    """
    # title, description, progress_status, assigned_by, assigned_to
    title = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=1000, blank=False)
    status = models.CharField(choices=status_fields, max_length=10, default='pp', blank=False)
    assign_to = models.ForeignKey(Uploader, blank=True)
    assigned_by = models.ForeignKey(MyUser, default=11, blank=False)
    assigned_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=timezone.now, blank=True)

    def __str__(self):
        return self.title
