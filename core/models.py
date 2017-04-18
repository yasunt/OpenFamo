from django.db import models

from .validators import validate_content


class TimeStampMixin(models.Model):
    created = models.DateTimeField(null=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HitsCountMixin(models.Model):

    def increment_hits(self):
        self.hits += 1
        return self.hits

    hits = models.IntegerField(default=0)

    class Meta:
        abstract = True


class ContentAbstractModel(models.Model):

    content = models.TextField(max_length=500, validators=[validate_content])

    @classmethod
    def get_average_content_length(cls):
        return True

    def get_content_length(self):
        return len(self.content)

    class Meta:
        abstract = True
