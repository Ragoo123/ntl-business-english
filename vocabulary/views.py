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

@login_required
def vocabulary_detail(request, folder_id, word_id):
    word = get_object_or_404(VocabularyWord, id=word_id, folder_id=folder_id)

    folder_words = VocabularyWord.objects.filter(folder_id=folder_id).order_by("id")

    word_list = list(folder_words)

    index = word_list.index(word)

    prev_word = word_list[index - 1] if index > 0 else None

    next_word = word_list[index + 1] if index < len(word_list) - 1 else None

    context = {
        "word": word,
        "folder": word.folder,
        "prev_word": prev_word,
        "next_word": next_word,
    }

    return render(request, "vocabulary/partials/_word-details.html", context)