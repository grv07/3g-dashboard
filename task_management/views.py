from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import Http404
from django.db.models import Q

from .forms import UserLoginForm, TaskAssignForm
from .models import Task
from content_uploader.models import Uploader
from classes.models import MyUser


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
                if user.is_staff:
                        return redirect('task_management:admin_dashboard')

                else:
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
    form = UserLoginForm(request.POST or None)
    return render(request, 'login.html', {'form': form})


def uploader_dashboard(request):
    """
    Dashboard for the uploader.
    :param request:
    :return:
    """
    uploader = Uploader.objects.filter(user_id=request.user.id).values_list('id', flat=True).get()
    tasks = Task.objects.filter(assign_to_id=uploader)
    return render(request, 'dashboard.html', {'tasks': tasks})


def admin_dashboard(request):
    """
    Dashboard for the admin.
    :param request:
    :return:
    """
    tasks = Task.objects.filter(assigned_by_id=request.user.id)
    perm = Permission.objects.filter(user=request.user)
    return render(request, 'admin_dashboard.html', {'tasks': tasks})


def assign_task(request):
    """
    To assign task to the uploader by the admin.
    :param request:
    :return:
    """
    print(request.POST)
    form = TaskAssignForm(request.POST or None)
    if form.is_valid():
        # instance = form.save(commit=False)
        # instance.status = 'ASSIGN'
        # instance.assigned_by = request.user.id
        # instance.save()
        return redirect('task_management:admin_dashboard')
    else:
        print(form)
    admin_users = MyUser.objects.filter(owner=request.user.id)
    return render(request, 'assign_task.html', {'form': form, 'admin_users': admin_users})


def edit_task(request, task_id):
    """
    To edit the task.
    :param request:
    :param task_id:
    :return:
    """
    user = request.user
    task = get_object_or_404(Task, pk=task_id)


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
        return redirect('task_management:admin_dashboard')
    else:
        raise Http404
