from django.shortcuts import render, get_object_or_404
from vocabulary.models import Folder, VocabularyWord
from django.http import HttpResponse
import random


def build_quiz_data(words):
    """Generate full quiz data list with shuffled options."""
    quiz_data = []

    for word in words:
        correct = word.definition
        all_defs = [w.definition for w in words if w.definition != correct]

        # Pick 3 incorrect options
        incorrect = random.sample(all_defs, min(3, len(all_defs)))

        # Combine and shuffle
        options = incorrect + [correct]
        random.shuffle(options)

        quiz_data.append({
            "id": word.id,
            "question": word.word,
            "options": options,
            "correct_answer": correct,
        })

    return quiz_data


def quizView(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    # Fetch & shuffle words
    words = list(VocabularyWord.objects.filter(folder=folder))
    random.shuffle(words)

    # Set basic session info
    request.session['folder_id'] = folder.id
    request.session['folder_name'] = folder.name

    # Load or create quiz_data
    if 'quiz_data' not in request.session:
        request.session['quiz_data'] = build_quiz_data(words)
        request.session['quiz_index'] = 0
        request.session['quiz_score'] = 0
        request.session.modified = True

    quiz_data = request.session['quiz_data']
    quiz_index = request.session.get('quiz_index', 0)

    current_question = quiz_data[quiz_index] if quiz_data else None

    context = {
        "folder_id": folder.id,
        "folder_name": folder.name,
        "current_question": current_question,
        "quiz_index": quiz_index + 1,
        "total_questions": len(quiz_data),
        "quiz_score": request.session.get('quiz_score', 0),
    }

    return render(request, "quiz/quiz.html", context)


def checkAnswer(request):
    return HttpResponse("ok")
