from django.db import models
from django.conf import settings

from django.db.models.signals import pre_save
from .signal import create_user_to_uploader


class Uploader(models.Model):
    """
    Uploader model for handle CRUD on uploading.
    """
    # TODO: Add some extra fields
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.user.username

pre_save.connect(create_user_to_uploader, sender=Uploader)
# Create your models here.
