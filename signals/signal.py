from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from course_managment.apps import CourseManagmentConfig

import time

def create_object_permission(app_label, model_name, per_codename, per_name):
    """
    Create permission on every object creations ...
    """
    content_type = ContentType.objects\
        .get(app_label=app_label.lower(), model=model_name.lower())
    permission = Permission.objects.create(codename=per_codename.lower(), \
        name=per_name.lower(), content_type=content_type)

    return permission

def update_user(sender, instance, **kwargs):
    # instance.user_permissions.save()
    permissions = Permission.objects.filter(user=instance)
    print(len(permissions), instance.user_permissions.all())

def create_course(sender, instance, **kwargs):
    #TODO: Call api when module create
    create_object_permission(app_label='course_managment', model_name=sender.__name__,\
        per_codename=instance.title, \
        per_name='crud | '+instance.title+' :'+str(instance.code)[:18])

def create_subject(sender, instance, **kwargs):
    #TODO: Call api when module create
    create_object_permission(app_label='course_managment', model_name=sender.__name__,\
        per_codename=instance.title, \
        per_name='crud | '+instance.title+' :'+str(instance.code)[:18])

def create_chapter(sender, instance, **kwargs):
    #TODO: Call api when module create
    create_object_permission(app_label='course_managment', model_name=sender.__name__,\
        per_codename=instance.title, \
        per_name='crud | '+instance.title+' :'+str(instance.code)[:18])

def create_topic(sender, instance, **kwargs):
    #TODO: Call api when module create
    create_object_permission(app_label='course_managment', model_name=sender.__name__,\
        per_codename=instance.title, \
        per_name='crud | '+instance.title+' :'+str(instance.code)[:18])

def create_module(sender, instance, **kwargs):
    #TODO: Call api when module create
    create_object_permission(app_label='course_managment', model_name=sender.__name__,\
        per_codename=instance.title, \
        per_name='crud | '+instance.title+' :'+str(instance.code)[:18])