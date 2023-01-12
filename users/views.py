from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate
from django.shortcuts import render, redirect
from logs.models import Log
from .forms import UserProfileForm
from datetime import date

# Create your views here.

def profile(request):
    today = date.today()
    logs = Log.objects.order_by('-id')[:5]
    context = {
        'today': today,
        'logs': logs,
    }
    return render(request, 'users/profile.html', context)

def configuration(request):
    form = UserProfileForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'users/configuration.html', context)

def changePhoto(request, id):
    form = UserProfileForm(request.POST)
    return redirect('users.configurations')

def changePassword(request):
    if request.method == 'POST':
        current_password=request.POST['current_password']
        new_password = request.POST['new_password']
        repeat_password = request.POST['repeat_new_password']
        non_empty_key = True if new_password != '' and repeat_password != '' else False
        if new_password == repeat_password and non_empty_key:
            user = authenticate(username=request.user, password=current_password)
            if user is not None:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'CLAVE ACTUALIZADA CON EXITO')
            else:
                messages.error(request, 'CLAVE ACTUAL INCORRECTA')
        else:
            messages.error(request, 'NUEVA CLAVE NO ES IGUAL ES LOS NUEVOS CAMPOS')
        
    return redirect(request.META.get('HTTP_REFERER'))