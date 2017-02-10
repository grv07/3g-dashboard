from django import forms
from .models import Task


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class TaskAssignForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    due_date = forms.DateField(required=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'assign_to', 'due_date']
