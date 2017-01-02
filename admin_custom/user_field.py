from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class MyUserCreationForm(UserCreationForm):
    """
    Form extends  UserCreationForm  for add email field.
    """
    email = forms.EmailField(label="Email", initial='@gmail.com')
    
    class Meta:
        model = User
        fields = ('email',)
