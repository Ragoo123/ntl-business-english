#urls.py
from django.urls import path
from .views import indexView, dashboardView


urlpatterns = [
    path('', indexView.as_view(), name='index'),
    path('dashboard/', dashboardView, name='dashboard'),
]