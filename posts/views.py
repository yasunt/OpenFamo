from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView, TemplateView
from django.views.generic.edit import FormMixin
from django.core.exceptions import PermissionDenied

from braces.views import LoginRequiredMixin, UserFormKwargsMixin
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView

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
        context = {'message': 'succeed'}
        return context


class QuestionListView(LoginFormMixin, QuestionCreateFormMixin, ListView):
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
            context['is_poster'] = True
            context['label'] = '質問を編集する'
        else:
            context['form'] = AnswerCreateForm
            context['label'] = '回答する'

        return context


class QuestionSearchView(TitleSearchMixin, ListView):
    model = Question


class UserRelatedCreateAPIView(LoginRequiredMixin, CreateAPIView):
    '''
    Base API view class for creating user-related objects via ajax.
    You have to define the class variable which is named serializer_class.
    And add fields to the instance variable which is named additional_fields,
    by overridding perform_create method in Inheriting view classes.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.additional_fields = {}

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            ValidationError('Unauthenticated User.')

        if self.additional_fields:
            serializer.save(user=user, **self.additional_fields)
        else:
            serializer.save(user=user)


class QuestionCreateAPIView(UserRelatedCreateAPIView):

    serializer_class = QuestionSerializer


class AnswerCreateAPIView(UserRelatedCreateAPIView):

    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        question = get_object_or_404(Question, id=self.request.POST['question_id'])
        self.additional_fields['question'] = question if question else False
        super().perform_create(serializer)


class PostUpdateAPIView(LoginRequiredMixin, RetrieveUpdateAPIView):
    '''
    It's a base API view class for updating objects via ajax.
    You have to define a class variable which is named serializer_class in inheriting view classes.
    '''

    serializer_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.additional_fields = {}

    def get(self, request, pk):
        self.object = self.get_object()
        return JsonResponse({'title': self.object.title, 'content': self.object.content})

    def post(self, request, pk):
        serializer = self.serializer_class(self.get_object(), data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer, request.user)
        return JsonResponse({'context': self.get_object().id})

    def perform_update(self, serializer, user):
        if self.additional_fields:
            serializer.save(user=user, **self.additional_fields)
        else:
            serializer.save(user=user)


class QuestionUpdateAPIView(PostUpdateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class LikeAPIView(UpdateView):

    model = Answer

    def post(self, request):
        answer = get_object_or_404(Answer, id=request.POST['answer_id'])
        if request.user.is_authenticated:
            if not request.user.like_answer.filter(id=request.POST['answer_id']).exists():
                answer.liked_by.add(request.user)
            else:
                answer.liked_by.remove(request.user)
        else:
            raise PermissionDenied

        return JsonResponse({'likes': answer.likes})

class LikeAPIView_(PostUpdateAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def post(self, request):
        self.object = get_object_or_404(Answer, id=request.POST['answer_id'])
        serializer = self.serializer_class(self.object, data={'content': 'like'})
        if serializer.is_valid():
            self.perform_update(serializer, request.user)
        return JsonResponse({})

    def perform_update(self, serializer, user):
        self.additional_fields['liked_by'] = [user]
        super().perform_update(serializer, user)

    def partial_update(self, request, *args, **kwargs):
        pass
