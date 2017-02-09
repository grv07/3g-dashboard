from django.conf.urls import url

from . import views

app_name = 'task_management'

urlpatterns = [
    url(r'^$', views.login_user, name='login'),
    url(r'^logout/$', views.login_user, name='logout'),
    url(r'^dashboard/$', views.uploader_dashboard, name='dashboard'),
    url(r'^admin_dashboard/$', views.admin_dashboard, name='admin_dashboard'),
    url(r'^(?P<task_id>[0-9]+)/$', views.edit_task, name='task'),
    url(r'^assign_task$', views.assign_task, name='assign_task'),
    url(r'^(?P<task_id>[0-9]+)/delete/$', views.delete_task, name='delete_task')
]
