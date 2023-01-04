from django.shortcuts import render
from .models import Alert
# Create your views here.

def index(request):
    alerts = Alert.objects.filter(status='WT').order_by('-created')[:20]
    context = {
        'alerts': alerts
    }
    return render(request, 'alerts/index.html', context)