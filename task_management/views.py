from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, get_user_model, login, logout

from .forms import UserLoginForm
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
                        return redirect('/tasks/admin_dashboard')
                else:
                    return redirect('/tasks/dashboard')
            else:
                return render(request, 'login.html', {'error_message': 'Account disabled'})
    else:
        return render(request, 'login.html')


def uploader_dashboard(request):
    uploader = Uploader.objects.filter(user_id=request.user.id).values_list('id', flat=True).get()
    tasks = Task.objects.filter(assign_to_id=uploader)
    return render(request, 'dashboard.html', {'tasks': tasks})


# def admin_dashboard(request):




def logout_user(request):
    """
    To logout the user and redirect to the login page.
    :param request:
    :return:
    """
    logout(request)
    form = UserLoginForm(request.POST or None)
    return render(request, 'login.html', {'form': form})


def edit_task(request, task_id):
    """
    To edit the task.
    :param request:
    :param task_id:
    :return:
    """
    user = request.user
    task = get_object_or_404(Task, pk=task_id)

