
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_publishes_recently_with_future_question(self):
        time = timezone.now()+datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now()-datetime.timedelta(days = 1,seconds = 1)
        old_question = Question(pub_date = time)

        self.assertIs(old_question.was_qullished_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now()-datetime.timedelta(hours=23,minutes=59,second=59)
        recent_question = Question(pub_date=time)

        self.asserIs(recent_question.was_published_recently(),True)



def create_question(question_text, days):
  
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        create_question(question_text="Future question.",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
