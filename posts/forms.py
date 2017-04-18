from django import forms
from django.db import models

from .models import Question, Answer


class QuestionCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ('title', 'content', 'user')


class AnswerCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ('title', 'content')
