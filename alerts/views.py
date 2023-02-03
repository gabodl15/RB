from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Alert
# Create your views here.

def index(request):
    # alerts = Alert.objects.filter(status='WT').order_by('-created')[:20]
    alerts = Alert.objects.values('color').distinct()
    alerts_by_color = {}

    for color in alerts:
        alerts_by_color[color['color']] = Alert.objects.filter(color=color['color']).exclude(status='SL')
    context = {
        'alerts_by_color': alerts_by_color
    }
    return render(request, 'alerts/index.html', context)

def attending(request, id):
    user = request.user
    alert = Alert.objects.get(id=id)
    alert.status = 'AT'
    alert.attended_by = user
    alert.save()
    return redirect('alerts.index')

def solved(request, id):
    alert = Alert.objects.get(id=id)
    alert.status = 'SL'
    alert.save()
    return redirect('alerts.index')

def delete(request, id):
    alert = Alert.objects.get(id=id)
    alert.delete()
    messages.success(request, 'Alerta Eliminada')
    return redirect('alerts.index')