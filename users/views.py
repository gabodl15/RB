from django.shortcuts import render
from logs.models import Log
from datetime import date

# Create your views here.

def profile(request):
    today = date.today()
    logs = Log.objects.order_by('-id')[:5]
    context = {
        'today': today,
        'logs':logs
    }
    return render(request, 'users/profile.html', context)
