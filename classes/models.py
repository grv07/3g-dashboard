from django.db import models
import uuid

name_defination = lambda title, code : title+"-"+str(code)[:8]


class ClassCategory(models.Model):
    """
    Manage Category Of classes.
    """
    created = models.DateTimeField(auto_now_add=True)
    
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # is_open = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Retrun course title and first 8 char"""
        return name_defination(self.title, self.code)


# Create your models here.
