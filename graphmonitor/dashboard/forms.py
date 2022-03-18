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

    class Meta:
        model = models.Commands
        fields = '__all__'


class DeviceForm(forms.ModelForm):
    class Meta:
        model = models.Devices
        fields = '__all__'
