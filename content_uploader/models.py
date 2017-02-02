from django.db import models
from django.conf import settings


class Uploader(models.Model):
    """
    Uploader model for handle CRUD on uploading.
    """
    # TODO: Add some extra fields
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.user.username

# Create your models here.
