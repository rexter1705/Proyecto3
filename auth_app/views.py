from django.shortcuts import render

def home(request):
    return render(request, 'auth_app/home.html')
