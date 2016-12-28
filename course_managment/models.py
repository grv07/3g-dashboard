from django.db import models

import uuid

name_defination = lambda title, code : title+"-"+str(code)[:8]

# ---Global MSG---
# Code is primary
# Order by created date 

class Course(models.Model):
    """Course class for CRUD"""
    title = models.CharField(max_length=100)
    class_category = models.ForeignKey('classes.ClassCategory', default=0)

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
    course = models.ForeignKey('Course', default=0)

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
    chapter = models.ForeignKey('Subject', default=0)

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
    topic = models.ForeignKey('Chapter', default=0)
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
    topic = models.ForeignKey('Topic', default=0)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500)

    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Retrun title and first 8 char"""
        return name_defination(self.title, self.code)                       
# Create your models here.