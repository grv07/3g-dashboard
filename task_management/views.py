from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, get_user_model, login, logout

from .forms import UserLoginForm


def login_user(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        return render(request, )
    else:
        return render(request, 'login.html', {'form': form})
