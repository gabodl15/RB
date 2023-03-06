from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, authenticate
from django.shortcuts import render, redirect
from clients.models import Client, Profile
from routers.models import Router, Plan
from nodos.models import CompanyAntenna
from logs.models import GlobalLog
from .forms import UserProfileForm
from .models import UserProfile
from datetime import date

# Create your views here.

def profile(request):
    if not hasattr(request.user, 'userprofile'):
        user = User.objects.get(id=request.user.id)
        obj = UserProfile.objects.create(
            user=user
        )
        obj.save()
    today = date.today()
    logs = GlobalLog.objects.filter(user=request.user).order_by('-id')[:5]
    context = {
        'today': today,
        'logs': logs,
    }

    if request.user.is_staff:

        active_profiles = Profile.objects.filter(agreement=False).exclude(plan__name='CORTADOS')
        clients = active_profiles.values_list('client', flat=True).distinct()
        agreements = Profile.objects.filter(agreement=True)
        cutting = Profile.objects.filter(plan__name='CORTADOS')
        routers = Router.objects.all()
        plans = Plan.objects.all()
        antennas = CompanyAntenna.objects.all()

        context['clients'] = clients
        context['agreements'] = agreements
        context['cutting'] = cutting
        context['routers'] = routers
        context['plans'] = plans
        context['antennas'] = antennas
    return render(request, 'users/profile.html', context)

def configuration(request):
    form = UserProfileForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'users/configuration.html', context)

def changePhoto(request, id):
    user = UserProfile.objects.get(id=id)
    form = UserProfileForm(request.POST, request.FILES)
    if form.is_valid():
        img = form.cleaned_data.get('avatar')
        user.avatar = img
        user.save()
    else:
        print(form.errors)
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