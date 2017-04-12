from django.shortcuts import render
from django.utils.functional import cached_property

from .models import Article


class PopularMixin(object):

    @cached_property
    def popular_articles(self):
        return {'popular_articles': Article.objects.popular(10)}


class ArticlesIndexView(PopularMixin):
    pass
