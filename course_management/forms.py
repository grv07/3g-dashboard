from .models import (Topic, Course, Subject)
from django import forms
from country_state.models import (Country, State)

GLOBAL_FORM_HIDE_LIST = ('is_live',)


class BasicCountryStateFilterForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, empty_label="Select Country")
    state = forms.ModelChoiceField(queryset=State.objects.none(), required=False, empty_label="Select State")

    class Meta:
        exclude = GLOBAL_FORM_HIDE_LIST


class TopicForm(BasicCountryStateFilterForm):
    stream = forms.ModelChoiceField(queryset=Course.objects.all(), required=False, empty_label="Select Stream")
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), required=False, empty_label="Select Subject")

    class Meta:
        model = Topic
        fields = ['country', 'state', 'stream', 'subject', 'chapter', 'title', 'description']

    def __init__(self, *args,  **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        print(self.fields['stream'])
        self.fields['subject'].queryset = Subject.objects.all()
