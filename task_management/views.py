from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import Http404
from django.db.models import Q

import json

from .forms import UserLoginForm, TaskAssignForm
from .models import Task
from content_uploader.models import Uploader, MyUser
from course_management.models import Course, Subject, Chapter, Topic, ModuleData


def login_user(request):
    """
    To login the user and get all the tasks of the user.
    :param request:
    :return: The list of tasks allotted to the user.
    """
    if request.method == 'POST':

        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user.is_active:
                login(request, user)
                return redirect('task_management:dashboard')

            else:
                return render(request, 'login.html', {'error_message': 'Account disabled'})

    else:
        return render(request, 'login.html')


def logout_user(request):
    """
    To logout the user and redirect to the login page.
    :param request:
    :return:
    """
    logout(request)
    return redirect('task_management:login')


def get_uploaders(request):
    admin_id = request.user.id
    uploader_list = MyUser.objects.filter(owner=admin_id)
    return render(request, 'select_uploader.html', {'uploader_list': uploader_list})


def dashboard(request):
    """
    Dashboard for the admin.
    :param request:
    :return:
    """
    if request.user.is_staff:
        tasks = Task.objects.filter(assigned_by_id=request.user.id)
        return render(request, 'admin_dashboard.html', {'tasks': tasks})
    else:
        tasks = Task.objects.filter(assign_to_id__user_id=request.user.id)
        return render(request, 'dashboard.html', {'tasks': tasks})


def assign_task(request, uploader_id):
    """
    To assign task to the uploader by the admin.
    :param request:
    :param uploader_id:
    :return:
    """
    print(request.POST)
    print('module_permission:', request.POST.get('module_permission'))
    form = TaskAssignForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.status = 'ASSIGN'
        task.assign_to_id = Uploader.objects.values_list('id', flat=True).get(user_id=uploader_id)
        task.assigned_by_id = request.user.id
        task.module_permission = ModuleData.objects.get(code=request.POST.get('module_permission'))
        task.save()
        return redirect('task_management:dashboard')
    else:
        print(form)
        # form = TaskAssignForm()

    course_data = []
    course_perms = Permission.objects.filter(content_type_id__model='course', user=uploader_id, name__contains='crud')

    for course in course_perms:
        course_name = course.name.split('| ')[-1]
        course_data.append(Course.objects.get(title__icontains=course_name))

    uploader_data = MyUser.objects.get(id=uploader_id)
    return render(request, 'assign_task.html', {'form': form, 'course_permissions': course_data, 'uploader': uploader_data})


def permissions(request, uploader_id):
    """
    Get the permissions allotted to the user.
    :param request:
    :return:
    """
    print('request data:', request.GET)
    # uploader_id = request.POST.get('uploader_id')
    print(uploader_id)
    subject_data = []
    chapter_data = []
    topic_data = []
    module_data = []

    subject_perms = Permission.objects.filter(content_type_id__model='subject', user=uploader_id, name__contains='crud')
    for subject in subject_perms:
        subject_name = subject.name.split(' | ')[-1]
        subject_data.append(Subject.objects.values('title', 'code').get(title__icontains=subject_name))
    chapter_perms = Permission.objects.filter(content_type_id__model='chapter', user=uploader_id, name__contains='crud')
    for chapter in chapter_perms:
        chapter_name = chapter.name.split('| ')[-1]
        chapter_data.append(Chapter.objects.values('title', 'code').get(title__icontains=chapter_name))
    topic_perms = Permission.objects.filter(content_type_id__model='topic', user=uploader_id, name__contains='crud')
    for topic in topic_perms:
        topic_name = topic.name.split('| ')[-1]
        topic_data.append(Topic.objects.values('title', 'code').get(title__icontains=topic_name))
    module_perms = Permission.objects.filter(content_type_id__model='moduledata', user=uploader_id, name__contains='crud')
    for module in module_perms:
        module_name = module.name.split('| ')[-1]
        module_data.append(ModuleData.objects.values('title', 'code').get(title__icontains=module_name))
    perms = {'subject_permissions': subject_perms, 'chapter_permissions': chapter_perms,
             'topic_permissions': topic_perms, 'module_permissions': module_perms}
    print(perms)
    return json.dumps(perms)


def edit_task(request, task_id):
    """
    To edit the task.
    :param request:
    :param task_id:
    :return:
    """
    task = get_object_or_404(Task, pk=task_id)
    form = TaskAssignForm(request.POST or None, instance=task)
    if form.is_valid():
        task = form.save(commit=False)
        task.status = 'ASSIGN'
        task.assign_to_id = request.POST.get('assign_to')
        task.assigned_by_id = request.user.id
        form.save()
        return redirect('task_management:dashboard')
    uploader_list = Uploader.objects.filter(user__owner=request.user.id)
    return render(request, 'assign_task.html', {'form': form, 'uploaders': uploader_list})


def delete_task(request, task_id):
    """
    To delete a task, can only be done by the admin or super-admin.
    :param request:
    :param task_id:
    :return:
    """
    if request.user.is_staff or request.user.is_superuser:
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        return redirect('task_management:dashboard')
    else:
        raise Http404

