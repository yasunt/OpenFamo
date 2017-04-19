from django import forms
from django.core.exceptions import ValidationError

from braces.forms import UserKwargModelFormMixin

from accounts.models import FamoUser


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = FamoUser
        fields = ('username', 'password')


class UserValidateFormMixin(UserKwargModelFormMixin, forms.ModelForm):

    def save(self, force_insert=False, force_update=False, commit=True):
        obj = super().save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
        return obj
