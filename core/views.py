from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required

# Create your views here.
class indexView(View):
    def get(self, request):        
        return render(request, "core/index.html")

@login_required
def dashboardView(request):
    return render(request, "core/dashboard.html")
