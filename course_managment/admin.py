from django.contrib import admin

from .models import Course, Subject, Chapter, Topic, ModuleData

admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Topic)
admin.site.register(ModuleData)
# Register your models here.
