from django.contrib import admin
from .models import Uploader
from classes.models import MyUser
from django.db.models import Q


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
        Filter user list according to owner access.
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
