#urls.py
from django.urls import path
from .views import indexView, dashboardView, vocabularyView


urlpatterns = [
    path('', indexView.as_view(), name='index'),
    path('dashboard/', dashboardView, name='dashboard'),
    path('vocabulary/', vocabularyView, name='vocabulary'),
]