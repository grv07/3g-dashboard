from django.db import models

import uuid

class ClassCategory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # is_open = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)

# Create your models here.
