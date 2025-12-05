from django.shortcuts import render
from django.views import View


# Create your views here.
class indexView(View):
    def get(self, request):        
        return render(request, "core/index.html")


class loginView(View):
    def get(self, request):        
        return render(request, "core/login.html")


class registerView(View):
    def get(self, request):
        return render(request, "core/register.html")