from django.contrib import admin
from .models import Course, Subject, Chapter, Topic, ModuleData

admin.site.register(Course)


def get_initial_return(request, _class, _parent_class):
    """
    :return: A dict to set initial value on form for drop-down.
    """
    parent_key = request.session.get('LS:'+_class.__name__, False)
    if parent_key:
        if _parent_class == 'course':
            return {
                'course': _class.objects.get(pk=parent_key).course.code,
            }
        elif _parent_class == 'subject':
            return {
                'subject': _class.objects.get(pk=parent_key).subject.code,
            }
        elif _parent_class == 'chapter':
            return {
                'chapter': _class.objects.get(pk=parent_key).chapter.code,
            }
        elif _parent_class == 'topic':
            return {
                'topic': _class.objects.get(pk=parent_key).topic.code,
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
