from django.conf.urls import url

from .views import QuestionListView, QuestionSearchView, QuestionDetailView
from .views import AnswerCreateAPIView, QuestionCreateAPIView, QuestionUpdateAPIView, LikeAPIView


app_name = 'posts'

urlpatterns = [
    url(r'^detail/(?P<pk>\d+)/$', QuestionDetailView.as_view(), name='detail'),
    url(r'^search/', QuestionSearchView.as_view(), name='search'),
    url(r'^create_question/$', QuestionCreateAPIView.as_view(), name='create_question'),
    url(r'^update_question/(?P<pk>\d+)/$', QuestionUpdateAPIView.as_view(), name='update_question'),
    url(r'^create_answer/$', AnswerCreateAPIView.as_view(), name='create_answer'),
    url(r'^like/$', LikeAPIView.as_view(), name='like'),
    url(r'^', QuestionListView.as_view(), name='list'),
]
