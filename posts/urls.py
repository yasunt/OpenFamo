from django.conf.urls import url

from .views import QuestionListView, QuestionSearchView, QuestionDetailView
from .views import QuestionCreateReadView, QuestionCreateUpdateView, QuestionReadUpdateDeleteView
from .views import AnswerCreateView


app_name = 'posts'

urlpatterns = [
    url(r'^detail/(?P<pk>\d+)/$', QuestionDetailView.as_view(), name='detail'),
    url(r'^search/', QuestionSearchView.as_view(), name='search'),
    url(r'^create_question/$', QuestionCreateUpdateView.as_view(), name='create_question'),
    url(r'^api/$', QuestionCreateReadView.as_view(), name='question_rest_api'),
    url(r'^api/(?P<title>[-\w+])/$', QuestionCreateReadView.as_view(), name='question_rest_api'),
    url(r'^good_button/', AnswerCreateView.as_view(), name='good_button'),
    url(r'^', QuestionListView.as_view(), name='list'),
]
