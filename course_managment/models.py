from django.db import models

import uuid

# Code is primary
class Course(models.Model):
    """Course class for CRUD"""
    created = models.DateTimeField(auto_now_add=True)
    
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)

    # is_open = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)

class Subject(models.Model):
    """Subject class for CRUD"""
    created = models.DateTimeField(auto_now_add=True)
    
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)

    # is_open = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)

class Chapter(models.Model):
    """Chapter class for CRUD"""
    created = models.DateTimeField(auto_now_add=True)
    
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)

    # is_open = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)

class Topic(models.Model):
    """Topic class for CRUD"""
    created = models.DateTimeField(auto_now_add=True)
    
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)

    # is_open = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)

class ModuleData(models.Model):
    """ModuleData class for CRUD"""
    created = models.DateTimeField(auto_now_add=True)
    
    title = models.CharField(max_length=100, blank=False)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)

    # is_open = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)                       
# Create your models here.