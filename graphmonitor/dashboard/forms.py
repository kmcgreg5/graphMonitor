from django import forms
from dashboard import models
from django.core.exceptions import ValidationError

class SwitchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SwitchForm, self).__init__(*args, **kwargs)
        self.fields['interval'].widget.attrs['placeholder'] = "HH:MM:SS"

    class Meta:
        model = models.Switches
        fields = '__all__'
        widgets = {'password': forms.PasswordInput()}


class CommandForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommandForm, self).__init__(*args, **kwargs)
        self.fields['query_interval'].widget.attrs['placeholder'] = "HH:MM:SS"

    # Checks that there are two or one capture groups depending on the unit selection
    def clean(self):
        cleaned_data = super().clean()
        query_unit = cleaned_data.get('query_unit')
        query_regex = cleaned_data.get('query_regex')
        
        num_capture_groups = query_regex.count("(") - query_regex.count("\(")
        
        if query_unit == 'auto':
            if num_capture_groups != 2:
                raise ValidationError('Exactly two capture groups must be defined in your regex when selecting "Auto" as the unit.')
        else:
            if num_capture_groups != 1:
                raise ValidationError('Exactly one capture group must be defined in your regex specifying a unit.')
        
        return cleaned_data


    class Meta:
        model = models.Commands
        fields = '__all__'


class DeviceForm(forms.ModelForm):
    class Meta:
        model = models.Devices
        fields = '__all__'
