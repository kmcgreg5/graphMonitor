from django import forms
from dashboard import models

class SwitchForm(forms.ModelForm):
    class Meta:
        model = models.Switches
        fields = '__all__'

class CommandForm(forms.ModelForm):
    class Meta:
        model = models.Commands
        fields = '__all__'
