from django.contrib import admin
from .models import Course, Subject, Chapter, Topic, ModuleData
from annoying.functions import get_object_or_None

admin.site.register(Course)


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
    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, Subject, 'course')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, Chapter, 'subject')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, Topic, 'chapter')


@admin.register(ModuleData)
class ModuleDataAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, ModuleData, 'topic')


# Register your models here.
