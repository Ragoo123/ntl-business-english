from django.shortcuts import render
from django.views import View

# Create your views here.
class LoginView(View):
    def get(self, request):        
        return render(request, "account/login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "account/register.html")