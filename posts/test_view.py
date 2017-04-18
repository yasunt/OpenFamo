from django.test import TestCase

from .views import QuestionCreateUpdateView
from .models import Question


class QuestionCreateTest(TestCase):

    def setup(self):
        self.question = Question(title='Question Create Test',
            content='This is a test case.')

    def test_list(self):
        question = Question.objects.get(id=self.question.id)
