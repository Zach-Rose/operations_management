from django import forms
from .models import Process, ProcessStep, Contributor


class ContributorForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = ['name']


class ProcessStepForm(forms.ModelForm):
    contributors = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'contributor-input',
            'autocomplete': 'off'
        }),
        help_text='Separate each contributor by a comma and space (e.g., John Doe, Jane Smith)'
    )
    duration_value = forms.IntegerField(
        widget=forms.NumberInput(attrs={'autocomplete': 'off'})
    )
    duration_unit = forms.ChoiceField(
        choices=[('seconds', 'Seconds'), ('minutes', 'Minutes'), ('days', 'Days')],
        widget=forms.Select(attrs={'autocomplete': 'off'})
    )

    class Meta:
        model = ProcessStep
        fields = ['name', 'duration_value', 'duration_unit', 'contributors']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'duration_value': forms.NumberInput(attrs={'autocomplete': 'off'}),
            'duration_unit': forms.Select(attrs={'autocomplete': 'off'}),
            'contributors': forms.TextInput(attrs={'autocomplete': 'off'})
        }


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['name', 'description', 'ideal_duration']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'autocomplete': 'off'}),
            'ideal_duration': forms.NumberInput(attrs={'autocomplete': 'off'})
        }
