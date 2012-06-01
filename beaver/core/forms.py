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

class BaseScheduleForm(forms.ModelForm):
    class Meta:
        model = models.BaseSchedule
        exclude = ('calendar')

class BookingForm(forms.ModelForm):
    class Meta:
        model = models.BaseSchedule

class BookingTypeForm(forms.ModelForm):
    class Meta:
        model = models.BookingType
        fields = ('title', 'description', 'length', 'price', 'currency', 'enabled')

class CalendarForm(forms.ModelForm):
    class Meta:
        model = models.Calendar
        fields = ('title', 'description', 'url', 'enabled')

class CalendarExceptEnabledForm(forms.ModelForm):
    class Meta:
        model = models.Calendar
        fields = ('title', 'description', 'url')

class ContactForm(forms.Form):
    subject = forms.CharField(max_length = 150)
    email_address = forms.EmailField()
    message = forms.CharField(widget = forms.Textarea)

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

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = models.Schedule
