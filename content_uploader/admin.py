from django.contrib import admin
from .models import Uploader
from django.db.models import Q

from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.forms import widgets
from admin_custom.user_field import MyUserCreationForm, MyUserChangeForm
from .models import MyUser

# from django.contrib.admin.models import LogEntry

# Unique email field of user
# User._meta.get_field('email')._unique = True


# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ('object_repr', 'change_message', 'user',)


class MyUserAdmin(UserAdmin):
    """
    This relation is important to read before any change:

    save_model: call on save a user object.

    get_queryset: Use to filter owners user.

    """
    def save_model(self, request, obj, form, change):
        """
        Add owner value on every user object.

        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.owner = request.user.id
        super(MyUserAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        If  user is super-admin:
            return all Users
        else:
            return only created users by request.user.

        :param request:
        :return: queryset
        """
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user.id)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'employee_number', 'employee_designation', 'password1',
                       'password2', 'department', 'type')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'type')

    def get_form(self, request, obj=None, **kwargs):
        """
        Filter permission list.

        if user is super-admin:
            can see or select from all permissions avail.
        elif user is admin:
            can select or allow his own restricted permissions to any other user.
        :param request:
        :param obj:
        :param kwargs:
        :return:
        """
        # Get form from original UserAdmin.
        form = super(MyUserAdmin, self).get_form(request, obj, **kwargs)
        if 'user_permissions' in form.base_fields:
            permissions = form.base_fields['user_permissions']
            if request.user.is_superuser:
                permissions.queryset = permissions.queryset.all()
            else:
                form.base_fields['is_active'].widget = widgets.HiddenInput()
                form.base_fields['is_staff'].widget = widgets.HiddenInput()
                form.base_fields['is_superuser'].widget = widgets.HiddenInput()
                permissions.queryset = permissions.queryset.filter(user=request.user)

        return form
    form = MyUserChangeForm
    add_form = MyUserCreationForm

admin.site.register(MyUser, MyUserAdmin)
# admin.site.register(LogEntry, LogEntryAdmin)
# Register your models here.


class UploaderAdmin(admin.ModelAdmin):
    """
    Create a uploader via admin panel.
    """
    def get_queryset(self, request):
        """
        Filter for show users that are own by request.user.

        :param request:
        :return:
        """
        qs = super(UploaderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user__owner=request.user.pk)

    def get_form(self, request, obj=None, **kwargs):
        """
        Filter user list

        return all avail_users for uploader creation.

        :param request:
        :param obj:
        :param kwargs:
        :return:
        """
        # Get form from original UserAdmin.
        form = super(UploaderAdmin, self).get_form(request, obj, **kwargs)
        if 'user' in form.base_fields:
            user = form.base_fields['user']
            # get all uploader with user id
            all_uploader_user_id = Uploader.objects.values_list('user_id', flat=True)
            # get all uploader created current user
            # ex: avail existing remaining user = (all created user)-(all users that are used before for uploader)
            user.queryset = MyUser.objects.filter(owner=request.user.id).filter(~Q(pk__in=all_uploader_user_id))

        return form

    exclude = ('is_superuser', 'is_staff')


admin.site.register(Uploader, UploaderAdmin)
# Register your models here.
