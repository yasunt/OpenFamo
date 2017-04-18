from django.forms import ModelForm

from accounts.models import FamoUser


class LoginForm(ModelForm):

    class Meta:
        model = FamoUser
        fields = ('username', 'password')
