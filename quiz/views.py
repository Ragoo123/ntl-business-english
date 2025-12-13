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
    #get data from POST
    selected_option = request.POST.get('selected_option')
    question_id = int(request.POST.get('question_id'))

    #retrieve quiz data from session
    quiz_data = request.session.get('quiz_data', [])
    quiz_index = request.session.get('quiz_index', 0)
    quiz_score = request.session.get('quiz_score', 0)
    folder_id = request.session.get('folder_id')
    folder_name = request.session.get('folder_name')

    #current question
    current_question = quiz_data[quiz_index]
    correct_answer = current_question['correct_answer']

    is_correct = False

    if selected_option == correct_answer:
        is_correct = True
        quiz_score += 1
        request.session['quiz_score'] = quiz_score\
        
    context = {
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "current_question": current_question,
        "quiz_index": quiz_index + 1,
        "total_questions": len(quiz_data),
        "quiz_score": quiz_score,
        "folder_id": folder_id,
        "folder_name": folder_name, 
        "selected_option": selected_option,      
    }

    return render(request, "partials/feedback_quiz_question.html", context)

def nextQuestion(request):
    #retrieve quiz data from session
    quiz_data = request.session.get('quiz_data', [])
    quiz_index = request.session.get('quiz_index', 0) + 1  #move to next question
    request.session['quiz_index'] = quiz_index
    request.session.modified = True

    folder_id = request.session.get('folder_id')
    folder_name = request.session.get('folder_name')

    if quiz_index >= len(quiz_data):
        #quiz is over
        context = {
            "quiz_score": request.session.get('quiz_score', 0),
            "total_questions": len(quiz_data),
            "folder_id": folder_id,
            "folder_name": folder_name,
            'percent': int((request.session.get('quiz_score', 0) / len(quiz_data)) * 100) if len(quiz_data) > 0 else 0,
            'incorrect': len(quiz_data) - request.session.get('quiz_score', 0),
        }
        return render(request, "quiz/quiz_finished.html", context)
    else:
        #next question
        current_question = quiz_data[quiz_index]
        context = {
            "current_question": current_question,
            "quiz_index": quiz_index + 1,
            "total_questions": len(quiz_data),
            "quiz_score": request.session.get('quiz_score', 0),
            "folder_id": folder_id,
            "folder_name": folder_name,
        }
        return render(request, "partials/_quiz_question.html", context)
