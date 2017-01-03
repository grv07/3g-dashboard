from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admin_custom.user_field import MyUserCreationForm
from django.contrib.auth.models import User
from .models import ClassCategory


# Unique email field of user
User._meta.get_field('email')._unique = True

admin.site.register(ClassCategory)
admin.site.unregister(User)


class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}),
    )

    add_form = MyUserCreationForm

admin.site.register(User, MyUserAdmin)
# Register your models here.
