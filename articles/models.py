from django.db import models

from core.models import TimeStampMixin, HitsCountMixin


class Article(TimeStampMixin, HitsCountMixin):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=100)
    url = models.URLField()
