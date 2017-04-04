from .models import (Chapter, Topic, Course, Subject)
from django import forms
from country_state.models import (Country, State)

GLOBAL_FORM_HIDE_LIST = ('is_live',)


class BasicCountryStateFilterForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, empty_label="--- Select One ---")
    state = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
    
    board = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
    grade = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')], attrs={'rows': 4, 'cols': 40}))

    class Meta:
        exclude = GLOBAL_FORM_HIDE_LIST


# class StreamForm(BasicCountryStateFilterForm):
#     stream = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
# 
#     class Meta:
#         model = Course
#         fields = ['country', 'state', 'board', 'grade',  'course', 'title', 'description']


class SubjectForm(BasicCountryStateFilterForm):
    stream = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))

    class Meta:
        model = Subject
        fields = ['country', 'state', 'board', 'grade',  'course', 'title', 'description']


class ChapterForm(BasicCountryStateFilterForm):
    stream = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
    
    class Meta:
        model = Chapter
        fields = ['country', 'state', 'board', 'grade', 'stream', 'subject', 'title', 'description']


class TopicForm(BasicCountryStateFilterForm):
    stream = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
    # subject = forms.ModelChoiceField(queryset=Subject.objects.none(), required=False, empty_label="Select Subject")
    subject = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))

    class Meta:
        model = Topic
        fields = ['country', 'state', 'board', 'grade', 'stream', 'subject', 'chapter', 'title', 'description']

