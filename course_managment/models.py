from django.db import models
from django.contrib.auth.models import User

import uuid

from signals import signal
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.urls import reverse
from django.utils.text import slugify

# from  django.db.models.signals.m2m_changed import post_add

name_defination = lambda title, code : title+"-"+str(code)[:8]
default_uuid = 'fd395736-523c-43bf-9653-cfe5ddd23528'

# ---Global MSG---
# Code is primary
# Order by created date

class Course(models.Model):
    """Course class for CRUD"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    class_category = models.ForeignKey('classes.ClassCategory', default=default_uuid)

    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)
    
    created = models.DateTimeField(auto_now_add=True)
    # is_open = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Retrun title and first 8 char"""
        return name_defination(self.title, self.code)


class Subject(models.Model):
    """Subject class for CRUD"""
    title = models.CharField(max_length=100, blank=True, default='')
    slug = models.SlugField(unique=True)
    course = models.ForeignKey('Course', default=default_uuid)

    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)
    
    created = models.DateTimeField(auto_now_add=True)
    # is_open = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Retrun title and first 8 char"""
        return name_defination(self.title, self.code)


class Chapter(models.Model):
    """Chapter class for CRUD"""
    title = models.CharField(max_length=100, blank=True, default='')
    slug = models.SlugField(unique=True)
    chapter = models.ForeignKey('Subject', default=default_uuid)

    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)
    
    created = models.DateTimeField(auto_now_add=True)
    # is_open = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Retrun title and first 8 char"""
        return name_defination(self.title, self.code)


class Topic(models.Model):
    """Topic class for CRUD"""
    title = models.CharField(max_length=100, blank=True, default='')
    slug = models.SlugField(unique=True)
    topic = models.ForeignKey('Chapter', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)

    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Retrun title and first 8 char"""
        return name_defination(self.title, self.code)  

class ModuleData(models.Model):
    """ModuleData class for CRUD"""
    title = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(unique=True)
    topic = models.ForeignKey('Topic', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)

    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Retrun title and first 8 char"""
        return name_defination(self.title, self.code)


pre_save.connect(signal.pre_save_create_slug, sender=Course)
pre_save.connect(signal.pre_save_create_slug, sender=Subject)
pre_save.connect(signal.pre_save_create_slug, sender=Chapter)
pre_save.connect(signal.pre_save_create_slug, sender=Topic)
pre_save.connect(signal.pre_save_create_slug, sender=ModuleData)
post_save.connect(signal.create_course, sender=Course)
post_save.connect(signal.create_subject, sender=Subject)
post_save.connect(signal.create_chapter, sender=Chapter)
post_save.connect(signal.create_topic, sender=Topic)
post_save.connect(signal.create_module, sender=ModuleData)

m2m_changed.connect(signal.update_user, sender=User.user_permissions.through)