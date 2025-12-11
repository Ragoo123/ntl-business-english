from django.shortcuts import render, get_object_or_404
from django.views import View
from vocabulary.models import Folder, VocabularyWord
import random
from django.http import HttpResponse

# Create your views here.
def quizView(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    words = list(VocabularyWord.objects.filter(folder=folder))
    random.shuffle(words)

    quiz_data = []

    for word in words:
        correct_answer = word.definition
        incorrect_options = [w.definition for w in words if w.definition != correct_answer]
        options = random.sample(incorrect_options, min(3, len(incorrect_options)))
        options.append(correct_answer)
        random.shuffle(options)

        quiz_data.append({
            'id': word.id,
            'question': word.word,
            'options': options,
            'correct_answer': correct_answer
        })

    request.session['folder_id'] = folder.id
    request.session['folder_name'] = folder.name

    if 'quiz_data' not in request.session:
    # generate quiz_data with shuffled options
        request.session['quiz_data'] = quiz_data
        request.session['quiz_index'] = 0
        request.session.modified = True
    else:
    # quiz_data already exists in session — do NOT regenerate
        quiz_data = request.session['quiz_data']

    quiz_index = request.session.get('quiz_index', 0)
    current_question = quiz_data[quiz_index] if quiz_data else None

    context = {
        "folder_id": folder.id,
        "folder_name": folder.name,
        'current_question': current_question,
    }
    return render(request, "quiz/quiz.html", context)


def checkAnswer(request):
    selected_option = request.POST.get('selected_option')
    question_id = request.POST.get('question_id')

    folder_id = request.session.get('folder_id')
    folder_name = request.session.get('folder_name')

    quiz_data = request.session.get('quiz_data', [])

    quiz_index = request.session.get('quiz_index', 0)
    current_question = quiz_data[quiz_index] if quiz_data else None

    correct_answer = current_question.get('correct_answer') if current_question else None

    is_correct = selected_option == correct_answer

    if is_correct:
        print("Correct Answer")
    else:
        print("Incorrect Answer")

    # common action
    request.session['quiz_index'] = quiz_index + 1
    request.session.modified = True

    # step 5: check bounds
    if request.session['quiz_index'] >= len(quiz_data):
        # quiz is finished
        return render(request, "quiz/quiz_finished.html")
    else:
        # quiz not finished, get next question
        next_question = quiz_data[request.session['quiz_index']]
        context = {
            'current_question': next_question,
            'folder_name': folder_name,
            'folder_id': folder_id, }
        
        return render(request, "partials/_quiz_question.html", context)


# #######################################################################
# def quizView(request, folder_id):
#     folder = get_object_or_404(Folder, id=folder_id)
#     words = VocabularyWord.objects.filter(folder=folder)
#     ranNum = random.randrange(len(words))

#     current_question_obj = words[ranNum]
#     question = current_question_obj.word
#     answer = current_question_obj.definition
#     question_id = current_question_obj.id
    
#     incorrect_options = []
#     for option in words:
#         if option.definition != answer:
#             incorrect_options.append(option.definition)
    
#     options = random.sample(incorrect_options, min(3, len(incorrect_options)))
#     options.append(answer)
#     random.shuffle(options)

#     # Save quiz data to session
#     request.session['current_quiz'] = {
#         "question": question,
#         "answer": answer,
#         "options": options,
#         "question_id": question_id,
#     }
#     request.session.modified = True


#     context = {
#         "folder": folder,
#         "words": words,
#         "question": question,
#         "answer": answer,
#         "options": options,
#         "question_id": question_id,
#     }

#     return render(request, "quiz/quiz.html", context)


# def checkAnswer(request):
#     selected_option = request.POST.get('selected_option')

#     quiz_data = request.session.get('current_quiz')
#     if not quiz_data:
#         return HttpResponse("No quiz in session", status=400)
    
#     correct_answer = quiz_data.get('answer')


#     if selected_option == correct_answer:
#         print("Correct answer!")
#     else:
#         print("Incorrect answer.")
   
#     return HttpResponse('ok')