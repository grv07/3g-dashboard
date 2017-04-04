from django.contrib import admin
from .models import (Course, Subject, Chapter, Topic, ModuleData)
from annoying.functions import get_object_or_None

from .forms import TopicForm

admin.site.register(Course)

GLOBAL_LIST_DISPLAY = ('get_title', 'is_live',)


def custom_queryset(self, request, _class):
    """
    Cutom query set for hidden on delete
    :param self:
    :param request:
    :param _class:
    :return:
    """
    qs = super(_class, self).get_queryset(request)
    if not request.user.is_superuser:
        qs = qs.filter(is_live=True)
    return qs


def get_initial_return(request, _class, _parent_class):
    """
    :return: A dict to set initial value on form for drop-down.
    """
    parent_key = request.session.get('LS:'+_class.__name__, False)
    if parent_key:
        if _parent_class == 'course':
            _obj = get_object_or_None(_class, pk=parent_key)
            return {
                'course': _obj.course.code if _obj else '',
            }
        elif _parent_class == 'subject':
            _obj = get_object_or_None(_class, pk=parent_key)
            return {
                'subject': _obj.subject.code if _obj else '',
            }
        elif _parent_class == 'chapter':
            _obj = get_object_or_None(_class, pk=parent_key)
            return {
                'chapter': _obj.chapter.code if _obj else '',
            }
        elif _parent_class == 'topic':
            _obj = get_object_or_None(_class, pk=parent_key)
            return {
                'topic': _obj.topic.code if _obj else '',
            }
        else:
            pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = GLOBAL_LIST_DISPLAY

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, SubjectAdmin)

    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, Subject, 'course')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = GLOBAL_LIST_DISPLAY

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, ChapterAdmin)

    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, Chapter, 'subject')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = GLOBAL_LIST_DISPLAY

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, TopicAdmin)

    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, Topic, 'chapter')

    def save_model(self, request, obj, form, change):
        """
        Add owner value on every user object.

        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        print(form.data)
        obj.owner = request.user.id
        print('Save now ..')
        super(TopicAdmin, self).save_model(request, obj, form, change)

    form = TopicForm


@admin.register(ModuleData)
class ModuleDataAdmin(admin.ModelAdmin):
    list_display = GLOBAL_LIST_DISPLAY

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, ModuleDataAdmin)

    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, ModuleData, 'topic')


# Register your models here.
