from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DeleteView, CreateView, DetailView, TemplateView
from django.views.generic.edit import FormMixin
from django.core.exceptions import PermissionDenied

from braces.views import LoginRequiredMixin, UserFormKwargsMixin
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from core.views import TitleSearchMixin, JsonResponseMixin, LoginFormMixin
from core.forms import LoginForm
from accounts.models import FamoUser
from .models import Answer, Question
from .forms import QuestionCreateForm, AnswerCreateForm
from .serializers import QuestionSerializer, AnswerSerializer


class QuestionCreateFormMixin(FormMixin):


    def get_form_class(self):
        if self.request.user.is_authenticated:
            return QuestionCreateForm
        else:
            return LoginForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = FamoUser.objects.get(id=self.request.user.id)
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AnswerCreateFormMixin(object):
    form_class = AnswerCreateForm


class AnswerCreateView(LoginRequiredMixin, JsonResponseMixin, AnswerCreateFormMixin, TemplateView):

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_data(self, context):
        print(self.request)
        context = {'message': 'succeed'}
        return context


class QuestionListView(LoginFormMixin, QuestionCreateFormMixin, ListView):
    # model = Question
    queryset = Question.objects.select_related()
    context_object_name = 'question_list'
    template_name = 'posts/question_list.html'

    def get_success_url(self):
        return reverse('posts:list')


class QuestionCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    models = Question
    form_class = QuestionCreateForm
    template_name = 'posts/detail.html'

    def get_success_url(self):
        return reverse('posts:detail')


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


class QuestionReadUpdateDeleteView(LoginRequiredMixin, RetrieveUpdateAPIView):
    # need to set a permission.

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'title'


class QuestionCreateAPIView(LoginRequiredMixin, CreateAPIView):

    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        print(self.request.POST)
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            ValidationError('Unauthenticated User.')
        serializer.save(user=user)


class AnswerCreateAPIView(LoginRequiredMixin, CreateAPIView):

    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            ValidationError('Unauthenticated User.')
        question = get_object_or_404(Question, id=self.request.POST['question_id'])
        serializer.save(user=user, question=question)


class AnswerEvaluateAPIView(LoginRequiredMixin, CreateAPIView):

    pass
