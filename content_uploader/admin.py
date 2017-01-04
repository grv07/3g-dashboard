from django.contrib import admin
from .models import Uploader


class UploaderAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(UploaderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user.pk)

    def save_model(self, request, obj, form, change):
        print(request.user)
        obj.admin_owner = [request.user]
        super(UploaderAdmin, self).save_model(request, obj, form, change)

    exclude = ('is_superuser', 'is_staff')


admin.site.register(Uploader, UploaderAdmin)

# Register your models here.
