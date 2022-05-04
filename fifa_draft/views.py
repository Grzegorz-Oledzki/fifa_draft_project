from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def create_group(request):
    return render(request, 'group-form.html')