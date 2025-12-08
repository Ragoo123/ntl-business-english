from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from vocabulary.models import Folder, VocabularyWord

# Create your views here.

@login_required
def vocabularyView(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    words = VocabularyWord.objects.filter(folder=folder)

    context = {
        "folder": folder,
        "words": words,
    }

    return render(request, "vocabulary/vocabulary.html", context)