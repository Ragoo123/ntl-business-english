from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def vocabularyView(request):
    return render(request, "vocabulary/vocabulary.html")