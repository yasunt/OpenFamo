from django.db import models

from accounts.models import FamoUser
from core.models import HitsCountMixin, TimeStampMixin
from .managers import PostManager


class Post(TimeStampMixin):

    def __str__(self):
        return self.title

    def count_length(self):
        return len(self.content)

    def is_poster(self, user):
        return True if self.user == user else False

    title = models.CharField(max_length=100)
    content = models.TextField(max_length=700)
    user = models.ForeignKey(FamoUser)

    objects = PostManager()

    class Meta:
        abstract = True


class Question(HitsCountMixin, Post):
    pass


class Answer(Post):
    question = models.ForeignKey(Question, null=True)
