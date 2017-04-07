
from django.contrib import admin
from .models import ClassCategory, BoardCategory
from .forms import CreateGradeFilterForm

import uuid
from constants.global_constant import GLOBAL_LIST_DISPLAY

# admin.site.register(ClassCategory)
admin.site.register(BoardCategory)


def custom_queryset(self, request, _class):
    """
    Custom query set for hidden on delete
    """
    qs = super(_class, self).get_queryset(request)
    if not request.user.is_superuser:
        qs = qs.filter(is_live=True)
    return qs


@admin.register(ClassCategory)
class BoardCategoryAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super(BoardCategoryAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, BoardCategoryAdmin)

    def save_model(self, request, obj, form, change):
        """
        User can select Multiple Grade:
        Add a new in form field as select_grade then loop on it and set obj grade
            and save obj in bulk.
        """
        grade_pk_list = form.data.getlist('select_grade')
        for grade_pk in grade_pk_list:
            obj.grade_id = grade_pk
            obj.owner = request.user.id
            obj.code = uuid.uuid4()
            obj.save()
    form = CreateGradeFilterForm
