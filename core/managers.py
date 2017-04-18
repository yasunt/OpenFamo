from django.db import models


class StatisticManager(models.Manager):

    use_for_related_fields = True

    def latest(self, num, **kwargs):
        return self.order_by('-created')[:num]

    def popular(self, num, **kwargs):
        return self.order_by('-hits')[:num]
