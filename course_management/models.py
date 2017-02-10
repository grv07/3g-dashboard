from django.db import models
import uuid

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, m2m_changed, pre_delete
import global_signal
from .signals import *
from django.contrib.admin.models import LogEntry
from classes.models import MyUser

name_defination = lambda title, parent_title: title+" | "+str(parent_title)[:18]
default_uuid = 'fd395736-523c-43bf-9653-cfe5ddd23528'
# ---Global MSG---
# Code is primary field
# Order by created date


class CommonInfo(models.Model):
    """
    Abstract class for reduce size of lines .. ;)
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(editable=False)
    description = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('created',)


class Course(CommonInfo):
    """
    Course class for CRUD
    """
    class_category = models.ForeignKey('classes.ClassCategory', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "1. Stream"
        verbose_name = "Stream"

    def __str__(self):
        """Retrun slug and first 8 char"""
        return name_defination(self.title, self.class_category)


class Subject(CommonInfo):
    """
    Subject class for CRUD
    """
    course = models.ForeignKey('Course', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "2. Subject"

    def __str__(self):
        """
        Return slug and first 8 char
        """
        return name_defination(self.title, self.course.title)


class Chapter(CommonInfo):
    """
    Chapter class for CRUD
    """
    subject = models.ForeignKey('Subject', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "3. Chapter"

    def __str__(self):
        """Return slug and first 8 char"""
        return name_defination(self.title, self.subject.title)


class Topic(CommonInfo):
    """
    Topic class for CRUD
    """
    chapter = models.ForeignKey('Chapter', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "4. Concept"

    def __str__(self):
        """
        Return slug and first 8 char
        """
        return name_defination(self.title, self.chapter.title)


class ModuleData(CommonInfo):
    """
    ModuleData class for CRUD
    """
    topic = models.ForeignKey('Topic', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "5. Module(s) Data"

    def __str__(self):
        """
        Return slug and first 8 char
        """
        return name_defination(self.title, self.topic.title)


for sender in [Course, Subject, Chapter, Topic, ModuleData]:
    """
    Calls pre-save function to create the slug field
    """
    pre_save.connect(pre_save_create_slug, sender=sender)
    pre_delete.connect(delete_object_permission, sender=sender)


# Connect global_signals with models here ...
pre_save.connect(global_signal.change_log_msg, sender=LogEntry)

post_save.connect(create_course, sender=Course)
post_save.connect(create_subject, sender=Subject)
post_save.connect(create_chapter, sender=Chapter)
post_save.connect(create_topic, sender=Topic)
post_save.connect(create_module, sender=ModuleData)

pre_save.connect(global_signal.change_user_type, sender=MyUser)

# User permissions edit
m2m_changed.connect(global_signal.update_user, sender=User.user_permissions.through)
post_save.connect(global_signal.send_mail_on_user_create, sender=User)
