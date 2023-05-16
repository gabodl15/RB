from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from clients.models import Client, Profile
from datetime import date, timedelta
import re

# Create your views here.
def index(request):
    today = date.today()
    
    clients_phone = Client.objects.filter(~Q(phone__isnull=True))
    clients = { client: re.sub(r'[\-. ]','',client.phone) for client in clients_phone }
    context = {
        'clients': clients,
    }
    return render(request, 'text_messages/index.html', context)

def send(request):
    if request.method == 'POST':
        messages.success(request, 'MENSAJES ENVIADOS')
    return redirect('text_messages.index')