from django.shortcuts import render, get_object_or_404, redirect
from vocabulary.models import Folder, VocabularyWord, QuizScore, User, ListeningQuiz, ListeningQuestion, ListeningOption
from quiz.models import ReadingText, ReadingQuestion, ReadingOption
from django.http import HttpResponse, Http404
import random

def quizReadingView(request, folder_id):
    folder = get_object_or_404(
        Folder.objects.prefetch_related(
            'reading_texts__questions__options'
        ),
        id=folder_id
    )

    current_folder_id = folder.id
    current_folder_name = folder.name
    print(current_folder_name)
    current_quiz_type = 'reading'
    session_folder_id = request.session.get('quiz_folder_id')

    reading_text = folder.reading_texts.first()
    print(type(reading_text), 'reading_text')
    
    if not reading_text:
        raise Http404("No reading text found for this folder.")

    quiz_data = request.session.get('quiz_data', [])
    quiz_index = request.session.get('quiz_index', 0)

    # --------------------------------------------
    # RESET if finished
    # --------------------------------------------
    if quiz_data and quiz_index >= len(quiz_data):
        for key in [
            'quiz_data', 'quiz_index', 'quiz_score',
            'quiz_folder_id', 'quiz_type'
        ]:
            request.session.pop(key, None)

        return redirect('quiz_reading', folder_id=folder.id)

    # --------------------------------------------
    # START NEW QUIZ
    # --------------------------------------------
    if (
        not quiz_data
        or session_folder_id != current_folder_id
        or request.session.get('quiz_type') != current_quiz_type
    ):
        questions = list(reading_text.questions.all())
        random.shuffle(questions)

        quiz_data = []

        for question in questions:
            options = list(question.options.all())
            random.shuffle(options)

            option_list = []

            for option in options:
                option_list.append({
                    'id': option.id,
                    'text': option.option_text
                })

            quiz_data.append({
                'id': question.id,
                'question_text': question.question_text,
                'options': option_list
            })

        request.session['quiz_data'] = quiz_data
        request.session['quiz_index'] = 0
        request.session['quiz_score'] = 0
        request.session['quiz_folder_id'] = current_folder_id
        request.session['folder_name'] = current_folder_name
        request.session['quiz_type'] = current_quiz_type
        request.session.modified = True

        quiz_index = 0

    # --------------------------------------------
    # CURRENT QUESTION
    # --------------------------------------------
    current_question = quiz_data[quiz_index]

    context = {
        'folder': folder,
        'reading_text': reading_text,
        'current_question': current_question,
        'quiz_index': quiz_index + 1,
        'total_questions': len(quiz_data),
        'quiz_score': request.session.get('quiz_score', 0),
        'quiz_partial': 'partials/_reading/_quiz_reading.html'
    }

    return render(request, 'quiz/quiz.html', context)



def checkAnswerReading(request):
    selected_option = int(request.POST.get('selected_option'))
    question_id = int(request.POST.get('question_id'))

    folder_id = request.session.get('quiz_folder_id')
    folder = Folder.objects.prefetch_related(
        'reading_texts__questions__options'
    ).get(id=folder_id)

    reading_text = folder.reading_texts.first()
    print(reading_text.text)
    quiz_score = request.session.get('quiz_score', 0)
    quiz_index = request.session.get('quiz_index', 0)
    folder_name = request.session.get('folder_name')
    quiz_data = request.session.get('quiz_data', [])
    current_question = quiz_data[quiz_index]
    options = current_question['options']
    
    selected_is_correct = ReadingOption.objects.filter(id=selected_option, question_id=question_id, is_correct=True).exists()
    
    for option in options:
        option['is_selected'] = option['id'] == selected_option
        option['is_correct'] = selected_is_correct and option['is_selected']

       

    if selected_is_correct:
        quiz_score += 1
        request.session['quiz_score'] = quiz_score
    else:
        print('wrong')
    
    quiz_index += 1
    request.session['quiz_index'] = quiz_index

    context = {
        'folder_name': folder_name,
        'quiz_score': quiz_score,
        'quiz_index': quiz_index,
        'total_questions': len(quiz_data),
        'is_correct': selected_is_correct,
        'current_question': current_question,
        'options': options,
        'reading_text': reading_text,
    }

    return render(request, "partials/_reading/_feedback_reading.html", context)




def quizViewListening(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    current_folder_id = folder.id
    session_folder_id = request.session.get('quiz_folder_id')
    current_quiz_type = 'listening'

    quiz_data = request.session.get('quiz_data', [])
    quiz_index = request.session.get('quiz_index', 0)

    # --------------------------------------------
    # RESET if finished
    # --------------------------------------------
    if quiz_data and quiz_index >= len(quiz_data):
        for key in [
            'quiz_data', 'quiz_index', 'quiz_score',
            'answered_questions', 'quiz_folder_id',
            'folder_id', 'folder_name', 'quiz_type',
            'audio_transcript', 'audio_url'
        ]:
            request.session.pop(key, None)

        return redirect('quiz_listening', folder_id=folder.id)

    # --------------------------------------------
    # START NEW QUIZ
    # --------------------------------------------
    if (
        not quiz_data
        or session_folder_id != current_folder_id
        or request.session.get('quiz_type') != current_quiz_type
    ):
        listening_quiz = ListeningQuiz.objects.filter(folder=folder).first()

        # Defensive check (prevents blank page)
        if not listening_quiz:
            return redirect('folder_list')

        # Store audio ONCE
        request.session['audio_url'] = (
            listening_quiz.audio_file.url
            if listening_quiz.audio_file else ""
        )
        request.session['audio_transcript'] = listening_quiz.transcript or ""

        questions = list(
            ListeningQuestion.objects.filter(listening_quiz=listening_quiz)
        )
        random.shuffle(questions)

        quiz_data = []

        for q in questions:
            options = list(q.options.all())
            random.shuffle(options)

            option_list = []
            correct_option_id = None
            correct_option_text = None

            for opt in options:
                option_list.append({
                    "id": opt.id,
                    "text": opt.option_text
                })
                if opt.is_correct:
                    correct_option_id = opt.id
                    correct_option_text = opt.option_text

            quiz_data.append({
                "id": q.id,
                "question_text": q.question_text,
                "options": option_list,
                "correct_option_id": correct_option_id,
                "correct_option_text": correct_option_text
            })
        print(quiz_data, "<<< quiz data")

        request.session['quiz_data'] = quiz_data
        request.session['quiz_index'] = 0
        request.session['quiz_score'] = 0
        request.session['quiz_folder_id'] = folder.id
        request.session['folder_id'] = folder.id
        request.session['folder_name'] = folder.name
        request.session['quiz_type'] = current_quiz_type
        request.session['answered_questions'] = []
        request.session.modified = True

        quiz_index = 0

    # --------------------------------------------
    # CURRENT QUESTION
    # --------------------------------------------
    current_question = quiz_data[quiz_index]

    context = {
        "folder_id": folder.id,
        "folder_name": folder.name,
        "current_question": current_question,
        "quiz_index": quiz_index + 1,
        "total_questions": len(quiz_data),
        "quiz_score": request.session.get('quiz_score', 0),
        "audio_url": request.session.get('audio_url', ""),
        "audio_transcript": request.session.get('audio_transcript', ""),
        "quiz_partial": "partials/_quiz_listening.html",
    }

    return render(request, "quiz/quiz.html", context)

def checkAnswerListening(request):
    selected_option = int(request.POST.get('selected_option'))
    selected_option_text = request.POST.get('selected_option_text')

    quiz_data = request.session.get('quiz_data', [])
    quiz_index = request.session.get('quiz_index', 0)
    quiz_score = request.session.get('quiz_score', 0)

    if quiz_index >= len(quiz_data):
        return redirect('quiz_listening', folder_id=request.session.get('folder_id'))

    current_question = quiz_data[quiz_index]
    correct_option_id = current_question['correct_option_id']

    is_correct = selected_option == correct_option_id

    if is_correct:
        quiz_score += 1
        request.session['quiz_score'] = quiz_score

    answered_questions = request.session.get('answered_questions', [])
    answered_questions.append({
        "question": current_question['question_text'],
        "selected_option": selected_option,
        "selected_option_text": selected_option_text,
        "correct_option": correct_option_id,
        "correct_option_text": current_question['correct_option_text'],
        
        "is_correct": is_correct,
    })
    request.session['answered_questions'] = answered_questions

    # advance index AFTER using current_question
    request.session['quiz_index'] = quiz_index + 1
    request.session.modified = True

    context = {
        "current_question": current_question,
        "options": current_question["options"],
        "selected_option": selected_option,
        "correct_option_id": correct_option_id,
        "is_correct": is_correct,
        "quiz_index": quiz_index + 1,
        "total_questions": len(quiz_data),
        "quiz_score": quiz_score,
        "folder_id": request.session.get('folder_id'),
        "folder_name": request.session.get('folder_name'),
        "audio_url": request.session.get('audio_url'),
        "audio_transcript": request.session.get('audio_transcript'),
    }

    return render(request, "partials/_feedback_listening.html", context)


def nextQuestionListening(request):
    quiz_data = request.session.get('quiz_data', [])
    quiz_index = request.session.get('quiz_index', 0)
    folder_id = request.session.get('folder_id')
    folder_name = request.session.get('folder_name')
    quiz_score = request.session.get('quiz_score', 0)
    answered_questions = request.session.get('answered_questions', [])
    current_question = quiz_data[quiz_index - 1]  # last question answered


    # --------------------------------------------
    # FINISHED QUIZ
    # --------------------------------------------
    if quiz_index >= len(quiz_data):
        folder = get_object_or_404(Folder, id=folder_id)

        save_best_score(
            user=request.user,
            folder=folder,
            quiz_type='listening',
            new_score=quiz_score
        )

        context = {
            "quiz_index": quiz_index,
            "quiz_data": quiz_data,
            "current_question": current_question,
            "answered_questions": answered_questions,
            "quiz_score": quiz_score,
            "total_questions": len(quiz_data),
            "folder_id": folder_id,
            "folder_name": folder_name,
            "incorrect": len(quiz_data) - quiz_score,
            "percent": int((quiz_score / len(quiz_data)) * 100) if quiz_data else 0,
            "quiz_review_partial": "partials/_review_answers_listening.html",
        }

        return render(request, "quiz/quiz_finished.html", context)
    

    # --------------------------------------------
    # NEXT QUESTION (FROM SESSION)
    # --------------------------------------------
    current_question = quiz_data[quiz_index]

    context = {
        "current_question": current_question,
        "quiz_index": quiz_index + 1,
        "total_questions": len(quiz_data),
        "quiz_score": quiz_score,
        "folder_id": folder_id,
        "folder_name": folder_name,
        "audio_url": request.session.get('audio_url', ''),
        "audio_transcript": request.session.get('audio_transcript', ''),
    }

    return render(request, "partials/_quiz_listening.html", context)



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

def save_best_score(user, folder, quiz_type, new_score):
    existing = QuizScore.objects.filter(
        user=user,
        folder=folder,
        quiz_type=quiz_type
    ).first()

    if existing:
        # Only update if new score is better
        if new_score > existing.score:
            existing.score = new_score
            existing.save()
    else:
        # No score yet → create one
        QuizScore.objects.create(
            user=user,
            folder=folder,
            quiz_type=quiz_type,
            score=new_score
        )

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
    current_quiz_type = 'vocabulary'



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
        request.session['quiz_type'] = 'vocabulary'
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
        user = request.user
        folder = get_object_or_404(Folder, id=folder_id)


        save_best_score(
            user=request.user,
            folder=folder,
            quiz_type=request.session.get('quiz_type', 'vocabulary'),
            new_score=request.session.get('quiz_score', 0)
        )
                
        context = {
            "quiz_score": request.session.get('quiz_score', 0),
            "total_questions": len(quiz_data),
            "folder_id": folder_id,
            "folder_name": folder_name,
            'percent': int((request.session.get('quiz_score', 0) / len(quiz_data)) * 100) if len(quiz_data) > 0 else 0,
            'incorrect': len(quiz_data) - request.session.get('quiz_score', 0),
            'answered_questions': answered_questions,
            "quiz_review_partial": "partials/_review_answers.html",
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




