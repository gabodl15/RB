from django.shortcuts import render
from datetime import date

# Create your views here.

def profile(request):
    today = date.today()
    context = {
        'today': today
    }
    return render(request, 'users/profile.html', context)
