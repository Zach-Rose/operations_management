from django import forms
from .models import Process, ProcessStep, Contributor


class ContributorForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = ['name']


from django import forms
from .models import ProcessStep

class ProcessStepForm(forms.ModelForm):
    name = forms.CharField(
        label='Activity Name',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    contributors = forms.CharField(
        label='Resources',
        widget=forms.TextInput(attrs={'class': 'resource-input'}),
        help_text='Separate each resource by a comma and space (e.g., John Doe, Jane Smith)'
    )
    duration_value = forms.IntegerField(
        label='Flow Time',
        widget=forms.NumberInput(attrs={'autocomplete': 'off'})
    )
    duration_unit = forms.ChoiceField(
        label='Flow unit',
        choices=[('seconds', 'Seconds'), ('minutes', 'Minutes'), ('days', 'Days')],
        widget=forms.Select(attrs={'autocomplete': 'off'})
    )
    steps = forms.CharField(
        label='Steps',
        widget=forms.Textarea(attrs={'autocomplete': 'off'}),
        required=False  # Make the steps field optional
    )

    class Meta:
        model = ProcessStep
        fields = ['name', 'duration_value', 'duration_unit', 'contributors', 'steps']


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['name', 'description', 'tack_time']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'autocomplete': 'off'}),
            'tack_time': forms.NumberInput(attrs={'autocomplete': 'off'})
        }