#urls.py
from django.urls import path
from .views import quizView, checkAnswer, nextQuestion, quizViewGapFill, quizViewListening,  checkAnswerListening, nextQuestionListening, quizReadingView, checkAnswerReading

urlpatterns = [
    path('quiz/<int:folder_id>/', quizView, name='quiz'),
    path('quiz/check/', checkAnswer, name='check_answer'),
    path('quiz/next/', nextQuestion, name='load_next_question'),
    path('quiz/<int:folder_id>/gapfill/', quizViewGapFill, name='quiz_gapfill'),
    path('quiz/<int:folder_id>/listening/', quizViewListening, name='quiz_listening'),
    path('quiz/check/listening/', checkAnswerListening, name='check_answer_listening'),
    path('quiz/next/listening/', nextQuestionListening, name='load_next_question_listening'),
    path('quiz/<int:folder_id>/reading/', quizReadingView, name='quiz_reading'),
    path('quiz/check/reading/', checkAnswerReading, name='check_answer_reading'),
    
]
