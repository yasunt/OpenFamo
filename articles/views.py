from django.shortcuts import render
from django.utils.functional import cached_property
from django.views.generic import CreateView, UpdateView

from braces.views import LoginRequiredMixin

from .models import Article, Comment
from .forms import CommentForm


class PopularMixin(object):

    @cached_property
    def popular_articles(self):
        return {'popular_articles': Article.objects.popular(10)}


class ArticlesIndexView(PopularMixin):
    pass


class CommentPostMixin(object):

    model = Comment
    fields = ('content', )


class CommentPostView(LoginRequiredMixin, CommentPostMixin, CreateView):

    form_class = CommentForm


class CommentUpdateView(LoginRequiredMixin, CommentPostMixin, UpdateView):

    form_class = CommentForm
