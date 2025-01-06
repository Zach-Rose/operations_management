from django import forms
from .models import Process, ProcessStep, Contributor


class ContributorForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = ['name']


class ProcessStepForm(forms.ModelForm):
    contributors = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'contributor-input'}),
        help_text='Separate each contributor by a comma and space (e.g., John Doe, Jane Smith)'
    )
    duration_value = forms.IntegerField()
    duration_unit = forms.ChoiceField(choices=[('seconds', 'Seconds'), ('minutes', 'Minutes'), ('days', 'Days')])

    class Meta:
        model = ProcessStep
        fields = ['name', 'duration_value', 'duration_unit', 'contributors']


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['name', 'description', 'ideal_duration']
