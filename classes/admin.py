from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admin_custom.user_field import MyUserCreationForm
from .models import ClassCategory
from classes.models import MyUser


admin.site.register(ClassCategory)

# Unique email field of user
# User._meta.get_field('email')._unique = True


class MyUserAdmin(UserAdmin):
    """
    This relation is important to read before any change:

    save_model: call on save a user object.
    get_queryset: Use to filter owners user.

    """

    def save_model(self, request, obj, form, change):
        """
        Use to add owner user on creation to a every user in admin dashboard system.
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
        If user is admin can see every one otherwise filter only created users.
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
            'fields': ('username', 'email', 'password1', 'password2')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Filter permission list according to users access
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
                permissions.queryset = permissions.queryset.filter(user=request.user)

        return form

    add_form = MyUserCreationForm

admin.site.register(MyUser, MyUserAdmin)
# Register your models here.
