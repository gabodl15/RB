import routeros_api.api
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django import http
from .models import Client, Profile, Log
from logs.models import GlobalLog
from routers.models import Router, Plan
from ventas.models import Referred
from .forms import ClientForm, ProfileForm
import folium

"""
ORDEN DEL ARCHIVO
- CLASES
    - ClientCreateView
- FUNCIONES
    - index
    - show
    - addProfile
    - editProfile
"""

class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    template_name = 'clients/create.html'
    success_url = '/clients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['referring_user'] = User.objects.all()
        return context

    def get_success_url(self):
        client = Client.objects.get(id=self.object.id)
        referred = self.request.POST.get('referred', 0)
        if referred:
            user = User.objects.get(id=referred)
            r = Referred(referred = user, client = client)
            r.save()
        return reverse('ventas.inspection.add', kwargs={'id': client.id})


def index(request):
    clients = Client.objects.all()
    return render(request, 'clients/index.html', {'clients': clients})

def show(request, id):
    client = Client.objects.get(id=id)
    coordinates = client.coordinates
    if coordinates:
        x = coordinates.split(',')
        map = folium.Map(location=[float(x[0]), float(x[1])], zoom_start=16)
        folium.Marker([float(x[0]), float(x[1])], tooltip='Clip aqui').add_to(map)
        map_render = map.get_root().render()
    else:
        map_render = None
    context = {
        'client': client,
        'map_render': map_render,
    }
    return render(request, 'clients/show.html', context)

def addProfile(request, id):
    client = Client.objects.get(id=id)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        router = Router.objects.get(id=request.POST['router'])
        plan = Plan.objects.get(id=request.POST['plan'])

        #SETIANDO LOS VALORES DEL FORMULARIO
        profile_name = request.POST['name']
        profile_password = request.POST['password']
        profile_mac = request.POST['mac']
        connection_mode = request.POST['connection_mode']
        cutoff_date = request.POST['cutoff_date'] if request.POST['cutoff_date'] != '' else None
        if form.is_valid():
            try:
                connection = routeros_api.api.RouterOsApiPool(
                    router.ip,
                    username=router.user,
                    password=router.password,
                    port=router.port,
                    plaintext_login=True,
                )
                api = connection.get_api()

                ### AGREGAR EL PPP AL MIKROTIK
                add_ppp = api.get_resource('/ppp/secret')
                add_ppp.add(
                    name=profile_name,
                    password=profile_password,
                    service='pppoe',
                    profile=plan.name
                )
                profile = Profile(
                    name=profile_name,
                    password=profile_password,
                    mac=profile_mac,
                    connection_mode=connection_mode,
                    cutoff_date=cutoff_date,
                    router=router,
                    plan=plan,
                    client=client
                )
                profile.save()
                global_log = GlobalLog(
                    user=request.user,
                    action='Add PPP',
                    message='Perfil {} ha sido creado con exito'.format(profile_name),
                )
                global_log.save()
                client_log = Log(
                    client=client,
                    action='Add PPP',
                    message='HA SIDO CREADO EL PPP {}'.format(profile),
                )
                client_log.save()
            except routeros_api.exceptions.RouterOsApiCommunicationError:
                messages.error(request, 'ERROR EN LA COMUNICACION CON EL ROUTER')
                return redirect(request.META.get('HTTP_REFERER'))
            except routeros_api.exceptions.RouterOsApiConnectionError:
                messages.error(request, 'NO PUDO CONECTAR CON EL ROUTER')
                return redirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(request, 'FORMULARIO NO VALIDO')
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('clients.show', id=id)
    form = ProfileForm()
    context = {
        'form': form,
        'client': client,
    }
    return render(request, 'clients/add_profile.html', context)

def editProfile(request, id):
    profile = Profile.objects.get(id=id)
    if request.method == 'POST':

        client = request.POST['client']
        new_name = request.POST['name']
        new_password = request.POST['password']
        new_mac = request.POST['mac']
        new_cutoff_date = request.POST['cutoff_date']
        new_router = Router.objects.get(id=request.POST['router'])
        new_plan = Plan.objects.get(id=request.POST['plan'])
        new_agreement = request.POST.get('agreement', False)

        try:
            connection = routeros_api.api.RouterOsApiPool(
                profile.router.ip,
                username=profile.router.user,
                password=profile.router.password,
                port=profile.router.port,
                plaintext_login=True,
            )
            api = connection.get_api()
            get_user = api.get_resource('/ppp/secret').get(name=profile.name)

            if profile.name != new_name:
                api.get_resource('/ppp/secret').set(id=get_user[0]['id'], name=new_name)
                profile.name = new_name

            if profile.password != new_password:
                api.get_resource('/ppp/secret').set(id=get_user[0]['id'], password=new_password)
                profile.password = new_password

            if profile.mac != new_mac:
                profile.mac = new_mac

            if profile.router != new_router:
                profile.router = new_router

            if profile.plan != new_plan:
                api.get_resource('/ppp/secret').set(id=get_user[0]['id'], profile=new_plan.name)
                profile.plan = new_plan

            if new_cutoff_date != '':
                profile.cutoff_date = new_cutoff_date

            if profile.agreement != new_agreement:
                profile.agreement = True if new_agreement == 'on' else False

            profile.save()

            connection.disconnect()

            global_log = GlobalLog(
                user=request.user,
                action='Edit PPP',
                message='PPP {} ha sido editado'.format(profile)
            )
            global_log.save()
            client_log = Log(
                client=profile.client,
                action='Edit PPP',
                message='PPP {} ha sido editado'.format(profile)
            )
            client_log.save()
        except routeros_api.exceptions.RouterOsApiCommunicationError:
            messages.error(request, 'ERROR EN LA COMUNICACION CON EL ROUTER')
            return redirect(request.META.get('HTTP_REFERER'))
        except routeros_api.exceptions.RouterOsApiConnectionError:
            messages.error(request, 'NO PUDO CONECTAR CON EL ROUTER')
            return redirect(request.META.get('HTTP_REFERER'))


        return redirect('clients.show', id=client)

    form = ProfileForm(instance=profile)
    context = {
        'profile': profile,
        'form': form
    }
    return render(request, 'clients/edit_profile.html', context)
