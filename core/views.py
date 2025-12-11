from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from vocabulary.models import Folder


# Create your views here.
class indexView(View):
    def get(self, request):        
        return render(request, "core/index.html")

@login_required
def dashboardView(request):
    folders = Folder.objects.all()  # everyone sees all folders

    context = {
        'folders': folders
    }
    return render(request, "core/dashboard.html", context)

