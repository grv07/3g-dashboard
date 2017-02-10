from django.contrib.auth.models import Permission
from utils import send_mail
from constants import mail_template_constants


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


def change_user_type(sender, instance, **kwargs):
    """
    Change type of user
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if instance.is_staff:
        instance.type = 'ADMIN'
    if instance.is_superuser:
        instance.type = 'SUPER-ADMIN'
    print('update/create user call ...')


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


def change_log_msg(sender, instance, **kwargs):
    msg = "Has been changed by {user}".\
        format(**{'user': instance.user})
    instance.change_message = msg
