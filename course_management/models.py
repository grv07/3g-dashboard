from django.db import models
from django.contrib.auth.models import User

import uuid

from signals import signal
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.urls import reverse

name_defination = lambda title, code : title+"-"+str(code)[:8]
default_uuid = 'fd395736-523c-43bf-9653-cfe5ddd23528'

# ---Global MSG---
# Code is primary field
# Order by created date


class CommonInfo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField(max_length=500)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('created',)
        # default_permissions = ()


class Course(CommonInfo):
    """
    Course class for CRUD
    """

    class_category = models.ForeignKey('classes.ClassCategory', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # is_open = models.BooleanField(default=False)
    
    class Meta(CommonInfo.Meta):
        pass

    def __str__(self):
        """Retrun title and first 8 char"""
        return name_defination(self.title, self.code)


class Subject(CommonInfo):
    """
    Subject class for CRUD
    """
    course = models.ForeignKey('Course', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        pass

    def __str__(self):
        """
        Return title and first 8 char
        """
        return name_defination(self.title, self.code)


class Chapter(CommonInfo):
    """
    Chapter class for CRUD
    """
    chapter = models.ForeignKey('Subject', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        pass

    def __str__(self):
        """Retrun title and first 8 char"""
        return name_defination(self.title, self.code)


class Topic(CommonInfo):
    """
    Topic class for CRUD
    """
    topic = models.ForeignKey('Chapter', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        pass

    def __str__(self):
        """
        Return title and first 8 char
        """
        return name_defination(self.title, self.code)  


class ModuleData(CommonInfo):
    """
    ModuleData class for CRUD
    """
    topic = models.ForeignKey('Topic', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        pass

    def __str__(self):
        """
        Return title and first 8 char
        """
        return name_defination(self.title, self.code)


# Calls pre save function to create the slug field
for sender in [Course, Subject, Chapter, Topic, ModuleData]:
    pre_save.connect(signal.pre_save_create_slug, sender=sender)

# Connect signals with models here ...
post_save.connect(signal.create_course, sender=Course)
post_save.connect(signal.create_subject, sender=Subject)
post_save.connect(signal.create_chapter, sender=Chapter)
post_save.connect(signal.create_topic, sender=Topic)
post_save.connect(signal.create_module, sender=ModuleData)

# User permissions edit
m2m_changed.connect(signal.update_user, sender=User.user_permissions.through)
post_save.connect(signal.send_mail_on_user_create, sender=User)