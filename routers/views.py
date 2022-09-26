from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import Router
from .forms import RouterForm, QueueForm, PppForm

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
    router = Router.objects.get(id = router)
    form = RouterForm(request.POST, instance = router)
    if form.is_valid():
        form.save()

    return redirect('routers.index')

def show(request, router):
    # ORDENAR
    # EL PRIMER PARAMETRO ES LA LISTA O DICCIONARIO A ORDENAR.
    # EL SEGUNDO PARAMETRO ES LA CLAVE POR LA QUE VA A ORDENAR
    def order(list_, key_):
        newlist = sorted(list_, key=lambda d: d[key_])
        return newlist

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
        usuarios = order(ppp.get(), 'name')

        queues_query = api.get_resource('/queue/simple')
        queues = order(queues_query.get(), 'name')

        ips_query = api.get_resource('/ip/address')

        ips = order(ips_query.get(), 'address')

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
        connection.disconnect()
        return render(request, 'routers/show.html', context)
    except ObjectDoesNotExist:
        messages.error(request, 'ROUTER NO REGISTRADO')

    except routeros_api.exceptions.RouterOsApiCommunicationError:
        messages.error(request, 'USUARIO O CLAVE INCORRECTOS')

    except routeros_api.exceptions.RouterOsApiConnectionError:
        messages.error(request, 'NO PUDO CONECTAR CON EL ROUTER')

    return redirect('routers.index')

def store(request):
    if request.method == 'POST':
        name = request.POST['name']
        ip = request.POST['ip']
        user = request.POST['user']
        password = request.POST['password']
        router = Router(name=name, ip=ip, user=user, password=password)
        router.save()
        messages.success(request, 'ROUTER GUARDADO CON EXITO')

    return redirect('routers.index')

def delete(request, router):
    if request.method == 'POST':
        router = Router.objects.get(id=router)
        router.delete()
        messages.success(request, 'ROUTER ELIMINADO CON EXITO')

    return redirect('routers.index')

def addQueue(request):
    if request.method == 'POST':
        form = QueueForm(request.POST)
        if form.is_valid():
            try:
                router = Router.objects.get(id=request.POST['router'])
                connection = routeros_api.RouterOsApiPool(
                    router.ip,
                    username=router.user,
                    password=router.password,
                    port=router.port,
                    plaintext_login=True,
                )
                api = connection.get_api()

                # REGISTRAR QUEUE
                add_queue = api.get_resource('/queue/simple')
                add_queue.add(
                    name = request.POST['name'],
                    max_limit = "512k/4M",
                    target = request.POST['target']
                )

                # TERMINAR CONEXION
                connection.disconnect()

                messages.success(request, 'QUEUE REGISTRADO CON EXITO')
                return redirect('routers.show', router.id)
            except ObjectDoesNotExist:
                messages.error(request, 'ROUTER NO REGISTRADO')
        else:
            messages.error(request, 'EL FORMULARIO NO ES VALIDO')
        return redirect(request.META.get('HTTP_REFERER'))

    previus_url = request.META.get('HTTP_REFERER')
    if '/routers/show/' in previus_url:
        get_router = previus_url.split('/routers/show/')
        print(get_router)
    form = QueueForm()
    return render(request, 'routers/queue/add.html', {'form': form})

def addPpp(request, router = False):
    if request.method == 'POST':
        print('POST')

    form = PppForm()
    if router:
        try:
            obj = Router.objects.get(id=router)
            connection = routeros_api.RouterOsApiPool(
                obj.ip,
                username=obj.user,
                password=obj.password,
                port=obj.port,
                plaintext_login=True,
            )
            api = connection.get_api()

            # GET PPP PROFILES
            profiles_ = api.get_resource('/ppp/profile')
            profiles = profiles_.get()

            # TERMINAR CONEXION
            connection.disconnect()
            list_ = [('default', 'default')]
            for item in profiles:
                list_.append((item['name'], item['name']))

            form.fields['profile'].choices = list_
        except ObjectDoesNotExist:
            messages.error(request, 'ROUTER NO REGISTRADO')

    return render(request, 'routers/ppp/add.html', {'form': form})
