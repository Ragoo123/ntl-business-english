from django.shortcuts import render, get_object_or_404, redirect
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

def build_gap_fill_data(words):
    """Generate full gap fill data list with shuffled options."""
    gap_fill_data = []

    for word in words:
        correct = word.word
        all_words = [w.word for w in words if w.word != correct]

        # Pick 3 incorrect options
        incorrect = random.sample(all_words, min(3, len(all_words)))

        # Combine and shuffle
        options = incorrect + [correct]
        random.shuffle(options)  

        sentence_with_blank = word.example_sentence.lower().replace(
            word.word,
            "_____",
            1  # replace only first occurrence
        )
      
        gap_fill_data.append({
            "id": word.id,
            "question": sentence_with_blank.strip().capitalize(),
            "options": options,
            "correct_answer": correct,
        })

    return gap_fill_data


def quizViewGapFill(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    # Identify current quiz context
    current_folder_id = folder.id
    session_folder_id = request.session.get('quiz_folder_id')
    current_quiz_type = 'gapfill'

    # Get quiz state safely
    gap_fill_quiz_data = request.session.get('quiz_data', [])
    gap_fill_quiz_index = request.session.get('quiz_index', 0)

       # --------------------------------------------
    # 🔴 CHANGE 1: If quiz is FINISHED and user refreshes
    # → reset quiz and start again
    # This prevents broken refresh on results page
    # --------------------------------------------
    if gap_fill_quiz_data and gap_fill_quiz_index >= len(gap_fill_quiz_data):
        request.session.pop('quiz_data', None)
        request.session.pop('quiz_index', None)
        request.session.pop('quiz_score', None)
        request.session.pop('answered_questions', None)
        request.session.pop('quiz_folder_id', None)
        request.session.pop('folder_id', None)
        request.session.pop('folder_name', None)
        request.session.pop('quiz_type', None)

        return redirect('quiz_gapfill', folder_id=folder.id)
    
    # --------------------------------------------
    # 🔴 CHANGE 2: Start a NEW quiz only if:
    # - No quiz exists OR
    # - Folder has changed
    # --------------------------------------------
    if not gap_fill_quiz_data or session_folder_id != current_folder_id or request.session.get('quiz_type') != current_quiz_type:
        words = list(VocabularyWord.objects.filter(folder=folder))
        random.shuffle(words)

        request.session['quiz_folder_id'] = current_folder_id
        request.session['quiz_data'] = build_gap_fill_data(words)
        request.session['quiz_index'] = 0
        request.session['quiz_score'] = 0
        request.session['folder_id'] = folder.id
        request.session['folder_name'] = folder.name
        request.session['answered_questions'] = []
        request.session['quiz_type'] = 'gapfill'
        request.session.modified = True

        gap_fill_quiz_data = request.session['quiz_data']
        gap_fill_quiz_index = 0  # reset index explicitly

        # --------------------------------------------
    # 🔴 CHANGE 3: Safe access after guards
    # --------------------------------------------
    current_question = gap_fill_quiz_data[gap_fill_quiz_index]

    context = {
        "folder_id": folder.id,
        "folder_name": folder.name,
        "gap_fill_data": gap_fill_quiz_data, 
        "current_question": current_question,
        "quiz_index": gap_fill_quiz_index + 1,
        "total_questions": len(gap_fill_quiz_data),
        "quiz_score": request.session.get('quiz_score', 0),
        "quiz_partial": "partials/_quiz_gapfill.html",
    }

    return render(request, "quiz/quiz.html", context)

def quizView(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    # Identify current quiz context
    current_folder_id = folder.id
    session_folder_id = request.session.get('quiz_folder_id')
    current_quiz_type = 'mcq'



    # Get quiz state safely
    quiz_data = request.session.get('quiz_data', [])
    quiz_index = request.session.get('quiz_index', 0)

    # --------------------------------------------
    # 🔴 CHANGE 1: If quiz is FINISHED and user refreshes
    # → reset quiz and start again
    # This prevents broken refresh on results page
    # --------------------------------------------
    if quiz_data and quiz_index >= len(quiz_data):
        request.session.pop('quiz_data', None)
        request.session.pop('quiz_index', None)
        request.session.pop('quiz_score', None)
        request.session.pop('answered_questions', None)
        request.session.pop('quiz_folder_id', None)
        request.session.pop('folder_id', None)
        request.session.pop('folder_name', None)
        request.session.pop('quiz_type', None)

        return redirect('quiz', folder_id=folder.id)

    # --------------------------------------------
    # 🔴 CHANGE 2: Start a NEW quiz only if:
    # - No quiz exists OR
    # - Folder has changed
    # --------------------------------------------
    if not quiz_data or session_folder_id != current_folder_id or request.session.get('quiz_type') != current_quiz_type:
        words = list(VocabularyWord.objects.filter(folder=folder))
        random.shuffle(words)

        request.session['quiz_folder_id'] = current_folder_id
        request.session['quiz_data'] = build_quiz_data(words)
        request.session['quiz_index'] = 0
        request.session['quiz_score'] = 0
        request.session['folder_id'] = folder.id
        request.session['folder_name'] = folder.name
        request.session['answered_questions'] = []
        request.session['quiz_type'] = 'mcq'
        request.session.modified = True

        quiz_data = request.session['quiz_data']
        quiz_index = 0  # reset index explicitly

    # --------------------------------------------
    # 🔴 CHANGE 3: Safe access after guards
    # --------------------------------------------
    current_question = quiz_data[quiz_index]

    # --------------------------------------------
    # Context for active quiz page
    # --------------------------------------------
    context = {
        "folder_id": folder.id,
        "folder_name": folder.name,
        "current_question": current_question,
        "quiz_index": quiz_index + 1,
        "total_questions": len(quiz_data),
        "quiz_score": request.session.get('quiz_score', 0),
        "quiz_partial": "partials/_quiz_question.html",
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
        request.session['quiz_score'] = quiz_score
    
    answer_record = {
        'question': current_question['question'],
        'correct_answer': current_question['correct_answer'],
        'selected_option': selected_option,
        'is_correct': is_correct
    }
    answered_questions = request.session.get('answered_questions', [])
    answered_questions.append(answer_record)
    request.session['answered_questions'] = answered_questions
        
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
    answered_questions = request.session.get('answered_questions', [])
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
            'answered_questions': answered_questions,
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
