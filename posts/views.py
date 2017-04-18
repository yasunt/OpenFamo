from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DeleteView, CreateView, DetailView, TemplateView
from django.views.generic.edit import FormMixin
from django.core.exceptions import PermissionDenied

from braces.views import LoginRequiredMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from core.views import TitleSearchMixin, JsonResponseMixin, LoginFormMixin
from core.forms import LoginForm
from accounts.models import FamoUser
from .models import Answer, Question
from .forms import QuestionCreateForm, AnswerCreateForm
from .serializer import QuestionSerializer


class QuestionCreateFormMixin(FormMixin):
    model = Question
    # form_class = QuestionCreateForm

    def get_form_class(self):
        if self.request.user.username:
            return QuestionCreateForm
        else:
            return LoginForm


class AnswerCreateFormMixin(object):
    form_class = AnswerCreateForm


class AnswerCreateView(LoginRequiredMixin, JsonResponseMixin, AnswerCreateFormMixin, TemplateView):

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_data(self, context):
        pass


class QuestionListView(LoginFormMixin, QuestionCreateFormMixin, ListView):
    # model = Question
    queryset = Question.objects.select_related()
    context_object_name = 'question_list'
    template_name = 'posts/question_list.html'

    def get_success_url(self):
        return reverse('posts:list')


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context['answers'] = question.answer_set.all()

        # form class depends on whether request user is question poster or not.
        if question.is_poster(self.request.user):
            context['form'] = QuestionCreateForm
        else:
            context['form'] = AnswerCreateForm

        return context


class QuestionCreateUpdateView(CreateView):
    model = Question
    template_name = 'posts/question_list.html'
    form_class = QuestionCreateForm

    def get_success_url(self):
        return reverse('posts:list')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class QuestionSearchView(TitleSearchMixin, ListView):
    model = Question


class QuestionCreateReadView(LoginRequiredMixin, ListCreateAPIView):
    # need to set a permission.

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'title'


class QuestionReadUpdateDeleteView(LoginRequiredMixin, RetrieveUpdateAPIView):
    # need to set a permission.

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'title'
