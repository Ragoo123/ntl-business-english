#urls.py
from django.urls import path
from .views import quizView, checkAnswer, nextQuestion

urlpatterns = [
    path('quiz/<int:folder_id>/', quizView, name='quiz'),
    path('quiz/check/', checkAnswer, name='check_answer'),
    path('quiz/next/', nextQuestion, name='load_next_question'),
]
