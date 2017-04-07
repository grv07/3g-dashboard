from django import forms
from country_state.models import Country
from .models import ClassCategory

GLOBAL_FORM_HIDE_LIST = ('is_live',)


def get_grade_with_unique_title():
    """
    To get distinct grade title to show on form.
    :return:
    """
    cc_list = ClassCategory.objects.distinct('title')
    return [(cc.code, cc.title) for cc in cc_list]


class BasicCountryStateFilterForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="--- Select One ---")
    state = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))
    board = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))
    title = forms.CharField(required=False, help_text="<b style='color:blue'>Create a new</b>")

    class Meta:
        exclude = GLOBAL_FORM_HIDE_LIST
        help_texts = {
            'title': 'Group to which this message belongs to',
        }


class CreateGradeFilterForm(BasicCountryStateFilterForm):
    add_with_grade = forms.MultipleChoiceField(required=False, choices=get_grade_with_unique_title(),
                                               widget=forms.CheckboxSelectMultiple,
                                               help_text=
                                               "<b style="
                                               "'color:blue;'>Select above checkbox "
                                               "to choose from existing grade.</b>")

    class Meta:
        model = ClassCategory
        fields = ['country', 'state', 'board', 'add_with_grade', 'title']
