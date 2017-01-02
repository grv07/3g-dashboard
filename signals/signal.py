from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from utils import send_mail
from constants import mail_template_constants


def create_object_permission(app_label, model_name, per_codename, per_name):
    """
    Create permission on every object creations ...
    """
    content_type = ContentType.objects.get(app_label=app_label.lower(), model=model_name.lower())
    permission = Permission.objects.create(codename=per_codename.lower(),
                                           name=per_name.lower(), content_type=content_type)

    return permission


def update_user(sender, instance, **kwargs):
    """
    Call when user permissions change via admin
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when user update
    """
    # Post add of permission.
    if kwargs.get('action', None) == 'post_add':
        permissions = Permission.objects.filter(user=instance)
        # TODO: Call api when update user permissions
    else:
        print('pre add call')


def create_course(sender, instance,  **kwargs):
    """
    Create a course permission that allow admin to permit a user for a course
    :param sender:
    :param instance:
    :param kwargs:
    :return: Call back API function when create a course
    """
    # TODO: Call api when module create
    create_object_permission(app_label='course_management', model_name=sender.__name__,
                             per_codename=instance.title,
                             per_name='crud | '+instance.title+' :'+str(instance.code)[:18])


def create_subject(sender, instance, **kwargs):
    """
    Create permission when create a subject of a course
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when subject create
    """
    # TODO: Call api when module create
    create_object_permission(app_label='course_management', model_name=sender.__name__,
                             per_codename=instance.title,
                             per_name='crud | '+instance.title+' :'+str(instance.code)[:18])


def create_chapter(sender, instance, **kwargs):
    """
    Create permission when create a chapter of a subject
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when chapter create
    """
    # TODO: Call api when module create
    create_object_permission(app_label='course_management', model_name=sender.__name__,
                             per_codename=instance.title,
                             per_name='crud | '+instance.title+' :'+str(instance.code)[:18])


def create_topic(sender, instance, **kwargs):
    """
    Create permission when create a Topic of a chapter
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when Topic create
    """
    # TODO: Call api when module create
    create_object_permission(app_label='course_management', model_name=sender.__name__,
                             per_codename=instance.title,
                             per_name='crud | '+instance.title+' :'+str(instance.code)[:18])


def create_module(sender, instance, **kwargs):
    """
    Create permission when create a Module of a topic
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when Module create
    """
    # TODO: Call api when module create
    create_object_permission(app_label='course_management', model_name=sender.__name__,
                             per_codename=instance.title,
                             per_name='crud | '+instance.title+' :'+str(instance.code)[:18])


def send_mail_on_user_create(sender, instance, **kwargs):
    """
    Call on post_save when user create
    :param sender:
    :param instance:
    :param kwargs:
    :return: Send an email on created user's email field.
    """
    register_subject = mail_template_constants.RESISTER_MSG.get('SUBJECT')
    register_body_template = mail_template_constants.RESISTER_MSG.get('MSG_BODY')
    register_body_template = register_body_template.format(user_name=instance.username, password=instance.password)
    send_mail(instance.email, register_subject, register_body_template)

