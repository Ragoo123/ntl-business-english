from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from vocabulary.models import Folder, QuizScore, ListeningQuestion


# Create your views here.
class indexView(View):
    def get(self, request):        
        return render(request, "core/index.html")

@login_required
def dashboardView(request):
    folders = Folder.objects.all()
    user = request.user
    user_scores = QuizScore.objects.filter(user=user)

    scores_map = {}

    for score in user_scores:
        folder_id = score.folder.id
        if folder_id not in scores_map:
            scores_map[folder_id] = {}
        scores_map[folder_id][score.quiz_type] = score.score

    for folder in folders:
        folder.scores = {
            'vocabulary': scores_map.get(folder.id, {}).get('vocabulary', 0),
            'gapfill': scores_map.get(folder.id, {}).get('gapfill', 0),
            'listening': scores_map.get(folder.id, {}).get('listening', 0),
            'reading': scores_map.get(folder.id, {}).get('reading', 0),
        }

    return render(request, "core/dashboard.html", {
        'folders': folders
    })

