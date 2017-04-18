from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import TimeStampMixin


class FamoUser(TimeStampMixin, AbstractUser):
    
    introduction = models.TextField(default='')
