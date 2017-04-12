from django.conf.urls import url
from .views import QuestionListView

app_name = 'posts'

urlpatterns = [
    url(r'^', QuestionListView.as_view(), name='list'),
]
