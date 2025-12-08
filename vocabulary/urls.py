from django.urls import path
from .views import vocabularyView

urlpatterns = [
      path('vocabulary/<int:folder_id>/', vocabularyView, name='vocabulary'),
]