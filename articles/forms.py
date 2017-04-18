from django import forms
from django.db import models

from core.validators import validate_content
from .models import Comment


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].validators.append(validate_content)

    class Meta:
        model = Comment
