from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admin_custom.user_field import MyUserCreationForm
from django.contrib.auth.models import User
from .models import ClassCategory

admin.site.register(ClassCategory)

# Unique email field of user
# User._meta.get_field('email')._unique = True

admin.site.unregister(User)


class MyUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(uploader__owner=request.user.id)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}),
    )

    def get_form(self, request, obj=None, **kwargs):
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

admin.site.register(User, MyUserAdmin)
# Register your models here.
