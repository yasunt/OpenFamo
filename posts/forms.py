from django import forms
from django.shortcuts import get_object_or_404
from django.db import models
from django.core.exceptions import ValidationError

from braces.forms import UserKwargModelFormMixin

from core.forms import UserValidateFormMixin
from accounts.models import FamoUser
from .models import Question, Answer
from .validators import validate_user


class QuestionCreateForm(UserValidateFormMixin, forms.ModelForm):

    class Meta:
        model = Question
        fields = ('title', 'content', )


class AnswerCreateForm(UserValidateFormMixin, forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('title', 'content')
