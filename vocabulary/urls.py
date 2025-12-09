from django.urls import path
from .views import vocabularyView, vocabulary_detail

urlpatterns = [
      path('vocabulary/<int:folder_id>/', vocabularyView, name='vocabulary'),
      path('vocabulary/<int:folder_id>/<int:word_id>/', vocabulary_detail, name='vocabulary_detail'),
]