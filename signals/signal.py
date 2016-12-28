from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from course_managment.apps import CourseManagmentConfig

def create_object_permission(app_label, model_name, \
                per_codename, per_name):
    content_type = ContentType.objects\
        .get(app_label=app_label.lower(), model=model_name.lower())

    permission = Permission.objects.create(codename=per_codename.lower(), \
        name=per_name.lower(), content_type=content_type)

    return True

def create_course(sender, instance, **kwargs):
    #TODO: Call api when module create
    print('Api Call succes ...', CourseManagmentConfig.name, sender.__name__)
    create_object_permission(app_label='course_managment', model_name=sender.__name__,\
        per_codename=instance.title, \
        per_name='crud | '+instance.title[:10]+' :'+str(instance.code)[:18])

def create_subject(sender, instance, **kwargs):
    #TODO: Call api when module create
    print('Api Call succes ...')
    create_object_permission(app_label='course_managment', model_name=sender.__name__,\
        per_codename=instance.title, \
        per_name='crud | '+instance.title[:10]+' :'+str(instance.code)[:18])

def create_chapter(sender, instance, **kwargs):
    #TODO: Call api when module create
    print('Api Call succes ...')
    create_object_permission(app_label='course_managment', model_name=sender.__name__,\
        per_codename=instance.title, \
        per_name='crud | '+instance.title[:10]+' :'+str(instance.code)[:18])

def create_topic(sender, instance, **kwargs):
    #TODO: Call api when module create
    print('Api Call succes ...')
    create_object_permission(app_label='course_managment', model_name=sender.__name__,\
        per_codename=instance.title, \
        per_name='crud | '+instance.title[:10]+' :'+str(instance.code)[:18])

def create_module(sender, instance, **kwargs):
    #TODO: Call api when module create
    print('Api Call succes ...')
    create_object_permission(app_label='course_managment', model_name=sender.__name__,\
        per_codename=instance.title, \
        per_name='crud | '+instance.title[:10]+' :'+str(instance.code)[:18])