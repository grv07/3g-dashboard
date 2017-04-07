from .models import (Chapter, Topic, Course, Subject)
from django import forms
from country_state.models import (Country)
from classes.models import ClassCategory

GLOBAL_FORM_HIDE_LIST = ('is_live',)


class BasicCountryStateFilterForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, empty_label="--- Select One ---")
    state = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
    
    board = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))

    class Meta:
        exclude = GLOBAL_FORM_HIDE_LIST


class BasicFilterWithGrade(BasicCountryStateFilterForm):
    grade = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))


class StreamForm(BasicCountryStateFilterForm):
    __all = ClassCategory.objects.all()
    select_grade = forms.ModelMultipleChoiceField(queryset=__all, widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        """
        Change Form: If dict has instance means its a change form.So, you can set initial value.
        and have fun
        """
        if 'instance' in kwargs:
            stream = kwargs['instance']
            initial = {'select_grade': ClassCategory.objects.filter(course__title=stream.title)}
            # self.fields['select_grade'].queryset = ClassCategory.objects.filter(course__title=stream.title)
            kwargs['initial'] = initial
        super(StreamForm, self).__init__(*args, **kwargs)
        # self.fields['select_grade'].queryset = ClassCategory.objects.filter(course__title=stream.title)

    class Meta:
        model = Course
        fields = ['country', 'state', 'board', 'select_grade', 'title', 'description']

    def clean_select_grade(self):
        select_grade_list = self.data.getlist('select_grade')
        print(self.data)
        error_on_grade = []
        for grade_pk in select_grade_list:
            if Course.objects.filter(title=self.data.get('title'), grade__code=grade_pk).exists():
                error_on_grade.append(ClassCategory.objects.get(pk=grade_pk).title)
            else:
                continue
        if error_on_grade:
            raise forms.ValidationError("Stream already exists for {0}".format(', '.join(error_on_grade)))
        return select_grade_list


class SubjectForm(BasicFilterWithGrade):
    stream = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))

    class Meta:
        model = Subject
        fields = ['country', 'state', 'board', 'grade',  'course', 'title', 'description']


class ChapterForm(BasicFilterWithGrade):
    stream = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
    
    class Meta:
        model = Chapter
        fields = ['country', 'state', 'board', 'grade', 'stream', 'subject', 'title', 'description']


class TopicForm(BasicFilterWithGrade):
    stream = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
    subject = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))

    class Meta:
        model = Topic
        fields = ['country', 'state', 'board', 'grade', 'stream', 'subject', 'chapter', 'title', 'description']

