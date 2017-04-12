from django.db import models


class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatisticManager(models.Manager):

    use_for_related_fields = True

    def latest(self, num, **kwargs):
        return self.order_by('-created')[:num]

    def popular(self, num, **kwargs):
        return self.order_by('-hits')[:num]


class HitsCountMixin(models.Model):

    def increment_hits(self):
        self.hits += 1
        return self.hits

    hits = models.IntegerField(default=0)

    class Meta:
        abstract = True
