#urls.py
from django.urls import path
from .views import quizView

urlpatterns = [
    path('quiz/', quizView, name='quiz'),
]
