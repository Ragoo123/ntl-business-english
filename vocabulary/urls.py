from django.urls import path
from .views import vocabularyView

urlpatterns = [
      path('vocabulary/', vocabularyView, name='vocabulary'),
]