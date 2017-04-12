from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView
from django.core.exceptions import PermissionDenied

from braces.views import LoginRequiredMixin

from accounts.models import FamoUser
from .models import Answer, Question


class QuestionListView(ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'posts/question_list.html'


class PostQuestionView(LoginRequiredMixin, CreateView):
    model = Question

    def form_valid(self, form):
        return super(PostQuestionView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PostQuestionView, self).form_invalid(form)


def authenticate(view_func):
    def authenticated_func(request, *args, **kwargs):
        if FamoUser.objects.filter(request.user.username).exists():
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return authenticated_func
