from .models import (Chapter, Topic, Course, Subject)
from django import forms
from classes.models import (ClassCategory, BoardCategory)
from classes.forms import (BasicCountryStateFilterForm, ChangeBasicCountryStateFilterForm)

from constants.global_constant import (MULTI_SELECT_GRADE_HELP, PRE_SELECT_GRADE_MSG)

from utils import (refile_form_from_hidden_fields, set_drop_downs_in_form)

GLOBAL_FORM_HIDE_LIST = ('is_live',)


# class BasicCountryStateFilterForm(forms.ModelForm):
#     country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, empty_label="--- Select One ---")
#     state = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
#
#     board = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
#
#     class Meta:
#         exclude = GLOBAL_FORM_HIDE_LIST


class BasicFilterWithGrade(BasicCountryStateFilterForm):
    select_grade = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))


class StreamForm(BasicCountryStateFilterForm):
    title = forms.CharField(required=True)
    select_grade = forms.CharField(widget=forms.CheckboxSelectMultiple, help_text=MULTI_SELECT_GRADE_HELP)

    class Meta:
        model = Course
        fields = ['country', 'select_state', 'select_board', 'select_grade', 'title', 'description']

    def clean_select_grade(self):
        select_grade_list = self.data.getlist('select_grade')
        error_on_grade = self._check_stream_grade_uniqueness(select_grade_list)

        if error_on_grade:
            raise forms.ValidationError("Stream already exists for {0}".format(', '.join(error_on_grade)))
        return select_grade_list

    def clean(self):
        cleaned_data = super(StreamForm, self).clean()
        refile_form_from_hidden_fields(self, grade_type={'type': 'multi_select'})
        title = self.data.get('title')
        select_grade_list = self.select_grade_clean(self.data.getlist('select_grade'))
        if not (select_grade_list or title):
            raise forms.ValidationError("Please select {0} or Fill {1} field.".format('Grade Checkbox', 'title'))
        return cleaned_data


class ChangeStreamForm(ChangeBasicCountryStateFilterForm):
    title = forms.CharField(required=True)
    # select_grade = forms.CharField(widget=forms.CheckboxSelectMultiple, help_text=MULTI_SELECT_GRADE_HELP)
    select_grade = forms.CharField(widget=forms.RadioSelect(),
                                   help_text='')

    def __init__(self, *args, **kwargs):
        """
        Change Form: If dict has instance means its a change form.So, you can set initial value.
        and have fun
        """
        if 'instance' in kwargs:
            stream_obj = kwargs['instance']
            selected_grade = stream_obj.grade
            selected_board = selected_grade.board
            selected_state = selected_board.state
            selected_country = selected_state.country

            initial = {'select_state': selected_state.id,
                       'title': stream_obj.title, 'country': selected_country.id,
                       'select_board': str(selected_board.code),
                       'select_grade': str(selected_grade.code),
                       }

            kwargs['initial'] = initial
        super(ChangeStreamForm, self).__init__(*args, **kwargs)
        # /// Common Functions
        country_state = selected_board.get_country_state_list()
        board_list = list(BoardCategory.objects.filter_by_state(selected_state))
        # //// .......
        avail_grades_in_selected_board = ClassCategory.objects.filter_by_board(selected_board)
        print(avail_grades_in_selected_board)

        _set_data = {'SELECT_STATE_OPTIONS': country_state.get('state_list', []), 'SELECT_BOARD_OPTIONS': board_list,
                     'SELECT_GRADE_OPTIONS': list(avail_grades_in_selected_board),
                     'grade': {'type': 'radio_select'}
                     }

        self.fields['select_grade'].help_text = PRE_SELECT_GRADE_MSG.format(selected_grade)
        set_drop_downs_in_form(self, **_set_data)

    class Meta:
        model = Course
        fields = ['country', 'select_state', 'select_board', 'select_grade', 'title', 'description']

    def clean_select_grade(self):
        select_grade_list = self.data.getlist('select_grade').remove('')
        error_on_grade = []
        if select_grade_list:
            select_grade_list.remove('')
            for grade_pk in select_grade_list:
                if Course.objects.filter(title=self.data.get('title'), grade__code=grade_pk).exists():
                    error_on_grade.append(ClassCategory.objects.get(pk=grade_pk).title)

        if error_on_grade:
            raise forms.ValidationError("Stream already exists for {0}".format(', '.join(error_on_grade)))
        return select_grade_list

    def clean(self):
        cleaned_data = super(ChangeStreamForm, self).clean()
        title = self.data.get('title')
        select_grade_list = self.select_grade_clean(self.data.getlist('select_grade'))
        if not (select_grade_list or title):
            raise forms.ValidationError("Please select {0} or Fill {1} field.".format('Grade Checkbox', 'title'))
        return cleaned_data


class SubjectForm(BasicFilterWithGrade):
    stream = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))

    class Meta:
        model = Subject
        fields = ['country', 'select_state', 'select_board', 'select_grade',  'course', 'title', 'description']


class ChapterForm(BasicFilterWithGrade):
    stream = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
    
    class Meta:
        model = Chapter
        fields = ['country', 'select_state', 'select_board', 'select_grade', 'stream', 'subject', 'title', 'description']


class TopicForm(BasicFilterWithGrade):
    stream = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
    subject = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))

    class Meta:
        model = Topic
        fields = ['country', 'select_state', 'select_board', 'select_grade', 'stream', 'subject', 'chapter', 'title', 'description']

