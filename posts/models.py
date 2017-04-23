from django.db import models
from django.utils.functional import cached_property

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

    @cached_property
    def likes(self):
        return self.liked_by.count()

    question = models.ForeignKey(Question, null=True)
    liked_by = models.ManyToManyField(FamoUser, related_name="like_answer")
