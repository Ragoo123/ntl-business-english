#urls.py
from django.urls import path
from . import views as core_views


urlpatterns = [
    path('', core_views.indexView.as_view(), name='index'),
    path('login/', core_views.loginView.as_view(), name='login'),
    path('register/', core_views.registerView.as_view(), name='register'),
]