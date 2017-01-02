from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", initial='@gmail.com')

    # def __init__(self, *args, **kwargs):
    #     self.field['email'].required = True
    #     super(MyUserCreationForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = User
        fields = ('email',)
