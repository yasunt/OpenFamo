from django.db import models

from accounts.models import FamoUser
from core.models import StatisticManager, HitsCountMixin


class PostManager(StatisticManager):
    pass


class Post(models.Model):

    def __str__(self):
        return self.title

    def count_length(self):
        return len(self.content)

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(FamoUser)

    objects = PostManager()

    class Meta:
        abstract = True


class Question(HitsCountMixin, Post):
    pass


class Answer(Post):
    pass
