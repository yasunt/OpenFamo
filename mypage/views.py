from django.shortcuts import render
from django.views.generic import DetailView

from braces.view import LoginRequiredMixin

from accounts.models import FamoUser
from posts.models import Question


class MypageIndexView(LoginRequiredMixin, DetailView):
    model = Question
