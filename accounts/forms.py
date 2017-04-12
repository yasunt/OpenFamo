from registration.forms import RegistrationForm

from .models import FamoUser


class FamoUserForm(RegistrationForm):
    
    class Meta:
        model = FamoUser
        fields  = RegistrationForm.Meta.fields
