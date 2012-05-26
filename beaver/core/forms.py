from django import forms
from core import models

class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')
        widgets = {
            'password': forms.widgets.PasswordInput,
        }
    
    confirm_password = forms.CharField(widget = forms.PasswordInput())

class AuthenticationForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('email', 'password')
        widgets = {
            'password': forms.widgets.PasswordInput,
        }

class CalendarForm(forms.ModelForm):
    class Meta:
        model = models.Calendar
        fields = ('title', 'description', 'url')

class EditAccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('first_name', 'last_name', 'password', 'confirm_password')
        widgets = {
            'password': forms.widgets.PasswordInput,
        }

    confirm_password = forms.CharField(widget = forms.PasswordInput())

class LostPasswordForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('email',)

class BaseScheduleForm(forms.ModelForm):
    class Meta:
        model = models.BaseSchedule
        exclude = ('calendar')

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = models.Schedule
