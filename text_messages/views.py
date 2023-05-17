from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from clients.models import Client, Profile
from routers.models import Router
from datetime import date, timedelta
import re, paramiko

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
        if request.user.userprofile.messages:
            routers = Router.objects.filter(sms__isnull=False)
            router = routers[0]
            ssh = paramiko.client.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(router.ip, username=router.user, password=router.password, allow_agent=False, look_for_keys=False)
            phones = request.POST.getlist('phones')
            message = request.POST['message']
            for phone in phones:
                command = f'/tool sms send port=usb3 phone-number={phone} message="{message}"'
                stdin, stdout, stderr = ssh.exec_command(command)
                salida = stdout.read().decode()
                error = stderr.read().decode()
            ssh.close()
            messages.success(request, 'MENSAJES ENVIADOS')
        else:
            messages.error(request, 'NO TIENES PERMISOS PARA ENVIAR MENSAJES.')
    return redirect('text_messages.index')