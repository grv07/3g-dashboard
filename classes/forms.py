from django import forms

# from django.shortcuts import get_object_or_404
from country_state.models import (Country)
from .models import (ClassCategory, BoardCategory)
from course_management.models import Course
from utils import (refile_form_from_hidden_fields, set_drop_downs_in_form)

from constants.global_constant import MULTI_SELECT_GRADE_HELP

GLOBAL_FORM_HIDE_LIST = ('is_live',)


def get_grade_with_unique_title():
    """
    To get distinct grade title to show on form.
    :return:
    """
    # cc_list = ClassCategory.objects.values_list('title', flat=True).distinct()
    # return [(cc, cc) for cc in cc_list]
    return []


class BasicFilterField(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="--- Select One ---")
    select_state = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))
    select_board = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))

    def select_grade_clean(self, select_grade_list):
        while '' in select_grade_list:
            select_grade_list.remove('')
        return select_grade_list

    def _check_stream_grade_uniqueness(self, select_grade_list):
        error_on_grade = []
        select_grade_list = self.select_grade_clean(select_grade_list)
        if select_grade_list:
            for grade_pk in select_grade_list:
                if Course.objects.filter(title=self.data.get('title'), grade__code=grade_pk).exists():
                    error_on_grade.append(ClassCategory.objects.get(pk=grade_pk).title)

        return error_on_grade


class BasicCountryStateFilterForm(BasicFilterField):
    """
    Hidden fields use to get save state of form on clean method.
    So, we can show it as a prepopulated fields with pre. filled values
    """
    hidden_select_state = forms.CharField(widget=forms.HiddenInput())
    hidden_select_board = forms.CharField(widget=forms.HiddenInput())
    hidden_select_grade = forms.CharField(widget=forms.HiddenInput())

    title = forms.CharField(required=False, help_text="<b style='color:blue'>Create a new</b>")

    def __init__(self, *args, **kwargs):
        """
        You can set initial value.
        """
        super(BasicCountryStateFilterForm, self).__init__(*args, **kwargs)

    class Meta:
        exclude = GLOBAL_FORM_HIDE_LIST
        help_texts = {
            'title': 'Group to which this message belongs to',
        }


class ChangeBasicCountryStateFilterForm(BasicFilterField):
    """
    Hidden fields use to get save state of form on clean method.
    So, we can show it as a prepopulated fields with pre. filled values
    """
    title = forms.CharField(required=False, help_text="<b style='color:blue'>Create a new</b>")

    def __init__(self, *args, **kwargs):
        """
        You can set initial value.
        """
        super(ChangeBasicCountryStateFilterForm, self).__init__(*args, **kwargs)

    class Meta:
        exclude = GLOBAL_FORM_HIDE_LIST
        help_texts = {
            'title': 'Group to which this message belongs to',
        }


class CreateGradeFilterForm(BasicCountryStateFilterForm):
    select_grade = forms.CharField(
        required=False, widget=forms.CheckboxSelectMultiple,
        help_text=MULTI_SELECT_GRADE_HELP)
        
    class Meta:
        model = ClassCategory
        fields = ['country', 'select_state', 'select_board', 'select_grade', 'title']

    def clean(self):
        cleaned_data = super(CreateGradeFilterForm, self).clean()
        refile_form_from_hidden_fields(self, grade_type={'type': 'multi_select'})
        title = self.data.get('title')
        select_grade_list = self.data.getlist('select_grade')
        if not (select_grade_list or title):
            raise forms.ValidationError("Please select {0} or Fill {1} field.".format('Grade Checkbox', 'title'))
        return cleaned_data


class ChangeGradeFilterForm(ChangeBasicCountryStateFilterForm):

    def __init__(self, *args, **kwargs):
        """
        Change Form: If dict has instance means its a change form. So, you can set initial value.
        and have fun
        """
        if 'instance' in kwargs:
            grade_obj = kwargs['instance']
            selected_board = grade_obj.board
            selected_state = selected_board.state
            initial = {'select_state': selected_state.id,
                       'title': grade_obj.title, 'country': '1',
                       'select_board': str(selected_board.code)
                       }
            kwargs['initial'] = initial

        super(ChangeGradeFilterForm, self).__init__(*args, **kwargs)
        # /// Common functions ...
        country_state = selected_board.get_country_state_list()
        board_list = list(BoardCategory.objects.filter_by_state(selected_state))
        # /// ....------
        set_data = {'SELECT_STATE_OPTIONS': country_state.get('state_list', []), 'SELECT_BOARD_OPTIONS': board_list,
                    'SELECT_GRADE_OPTIONS': [], 'grade': {'type': 'multi_select'}}
        set_drop_downs_in_form(self, **set_data)

    class Meta:
        model = ClassCategory
        fields = ['country', 'select_state', 'select_board', 'title']

    def clean(self):
        cleaned_data = super(ChangeGradeFilterForm, self).clean()
        title = self.data.get('title', None)
        board_pk = self.data.get('select_board', None)

        if title:
            if board_pk:
                try:
                    ClassCategory.objects.get(board__pk=board_pk, title=title)
                except ClassCategory.DoesNotExist:
                    pass
                else:
                    raise forms.ValidationError("Grade already exist with this title and board.")
        else:
            raise forms.ValidationError("Please select {0} or Fill {1} field.".format('Grade Checkbox', 'title'))

        return cleaned_data



