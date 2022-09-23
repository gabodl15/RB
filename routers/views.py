from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Router
from .forms import RouterForm

import routeros_api

def index(request):
    routers = Router.objects.all()
    return render(request, 'routers/index.html', {'routers': routers})

def create(request):
    form = RouterForm()
    return render(request, 'routers/create.html', {'form': form})

def edit(request, id):
    if request.method == 'POST':
        router = get_object_or_404(Router, id = id)
        form = RouterForm(instance = router)
        return render(request, 'routers/edit.html', {'form': form, 'router': router})

def update(request, router):
    router = get_object_or_404(Router, id = router)
    form = RouterForm(instance = router)
    if form.is_valid():
        form.save()

    return redirect('routers.index')


def show(request, router):
    try:
        router = Router.objects.get(id=router)
        connection = routeros_api.RouterOsApiPool(
            router.ip,
            username=router.user,
            password=router.password,
            port=router.port,
            plaintext_login=True,
        )
        api = connection.get_api()

        #identity
        identity_query = api.get_resource('/system/identity')
        identity = identity_query.get()

        #routerboard
        resource_query = api.get_resource('/system/resource')
        resource = resource_query.get()

        #health
        health_query = api.get_resource('/system/health')
        health = health_query.get()

        interfaces_query = api.get_resource('/interface/ethernet')
        interfaces = interfaces_query.get()

        ppp = api.get_resource('/ppp/secret')
        usuarios = ppp.get()

        queues_query = api.get_resource('/queue/simple')
        queues = queues_query.get()

        ips_query = api.get_resource('/ip/address')
        ips = ips_query.get()

        context = {
            'router': router,
            'identity': identity,
            'interfaces': interfaces,
            'health': health,
            'resource': resource,
            'usuarios': usuarios,
            'queues': queues,
            'ips': ips
        }

        return render(request, 'routers/show.html', context)
    except ObjectDoesNotExist:
        return render(request, 'routers/show.html', {'message': 'ROUTER NO REGISTRADO'})
    except routeros_api.exceptions.RouterOsApiCommunicationError:
        return render(request, 'routers/show.html', {'message': 'USUARIO O CLAVE INCORRECTO'})

def store(request):
    if request.method == 'POST':
        name = request.POST['name']
        ip = request.POST['ip']
        user = request.POST['user']
        password = request.POST['password']
        router = Router(name=name, ip=ip, user=user, password=password)
        router.save()

    return redirect('routers.index')

def delete(request, router):
    if request.method == 'POST':
        router = Router.objects.get(id=router)
        router.delete()

        return redirect('routers.index')

    else:
        return redirect('routers.index')
