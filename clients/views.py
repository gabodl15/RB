from django.shortcuts import render

def index(request):
    return render(request, 'clients/index.html', {})

def create(request):
    return render(request, 'clients/create.html', {})
