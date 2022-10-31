from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Router, Plan
from .forms import RouterForm, QueueForm, PppForm, AddressFrom

import routeros_api, folium

### ESTABLECEMOS CONEXION CON EL ROUTER
def router_connection(request, id):
    try:
        router = Router.objects.get(id=id)
        connection = routeros_api.RouterOsApiPool(
            router.ip,
            username=router.user,
            password=router.password,
            port=router.port,
            plaintext_login=True,
        )
        api = connection.get_api()
        return connection, api, router
    except ObjectDoesNotExist:
        messages.error(request, 'ROUTER NO REGISTRADO')
    except routeros_api.exceptions.RouterOsApiCommunicationError:
        messages.error(request, 'USUARIO O CLAVE INCORRECTOS')
    except routeros_api.exceptions.RouterOsApiConnectionError:
        messages.error(request, 'NO PUDO CONECTAR CON EL ROUTER')
    return redirect(request.META.get('HTTP_REFERER')), 0, 0

def router_disconnection(connection):
    # TERMINAR CONEXION
    connection.disconnect()

def index(request):
    routers = Router.objects.all()
    return render(request, 'routers/index.html', {'routers': routers})

def show(request, id):
    # ORDENAR
    """
    - EL PRIMER PARAMETRO ES LA LISTA O DICCIONARIO A ORDENAR.
    - EL SEGUNDO PARAMETRO ES LA CLAVE POR LA QUE VA A ORDENAR
    """
    def order(list_, key_):
        newlist = sorted(list_, key=lambda d: d[key_])
        return newlist

    connection, api, router = router_connection(request, id)
    if isinstance(connection, HttpResponseRedirect):
        return connection

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

    if router.nodo:
        coordinates = router.nodo.coordinates
        x = coordinates.split(',')
        map = folium.Map(location=[float(x[0]), float(x[1])], zoom_start=16)
        folium.Marker([float(x[0]), float(x[1])], tooltip='Clip aqui').add_to(map)
        map_render = map.get_root().render()
    else:
        map_render = None

    context = {
        'router': router,
        'identity': identity,
        'interfaces': interfaces,
        'health': health,
        'resource': resource,
        'usuarios': usuarios,
        'queues': queues,
        'ips': ips,
        'map': map_render
    }

    router_disconnection(connection)
    return render(request, 'routers/show.html', context)

def addQueue(request, id):
    connection, api, router = router_connection(request, id)
    if isinstance(connection, HttpResponseRedirect):
        return connection

    if request.method == 'POST':
        form = QueueForm(request.POST)
        if form.is_valid():


            # REGISTRAR QUEUE
            add_queue = api.get_resource('/queue/simple')
            add_queue.add(
                name = request.POST['name'],
                max_limit = request.POST['upload'] + '/' + request.POST['download'],
                target = request.POST['target']
            )

            # TERMINAR CONEXION
            router_disconnection(connection)

            messages.success(request, 'QUEUE REGISTRADO CON EXITO')
            return redirect('routers.show', router.id)
        else:
            messages.error(request, 'EL FORMULARIO NO ES VALIDO')
            return redirect(request.META.get('HTTP_REFERER'))

    form = QueueForm()
    context = {
        'form': form,
        'router': router
    }
    return render(request, 'routers/queue/add.html', context)

def addPpp(request, id):
    connection, api, router = router_connection(request, id)
    if isinstance(connection, HttpResponseRedirect):
        return connection

    if request.method == 'POST':
        # REGISTRANDO PPP
        add_ppp = api.get_resource('/ppp/secret')
        add_ppp.add(
            name=request.POST['name'],
            service='pppoe',
            password=request.POST['password'],
            profile=request.POST['profile'],
        )

        # TERMINAR CONEXION
        router_disconnection(connection)

        messages.success(request, 'PPP REGISTRADO CON EXITO')
        return redirect('routers.show', id)

    # GET PPP PROFILES
    profiles_ = api.get_resource('/ppp/profile')
    profiles = profiles_.get()

    # TERMINAR CONEXION
    router_disconnection(connection)
    list_ = []
    for item in profiles:
        list_.append((item['name'], item['name']))

    form = PppForm()
    form.fields['profile'].choices = list_

    context = {
        'form': form,
        'router': router
    }
    return render(request, 'routers/ppp/add.html', context)

def addAddress(request, id):
    connection, api, router = router_connection(request, id)
    if isinstance(connection, HttpResponseRedirect):
        return connection

    if request.method == 'POST':
        # REGISTRAR ADDRESS
        add_address = api.get_resource('/ip/address')
        add_address.add(
            address = request.POST['address'],
            network = request.POST['network'],
            interface = request.POST['interface']
        )

        messages.success(request, 'ADDRESS AGREGADO CON EXITO')
        return redirect('routers.show', id)

    # GET INTERFACES
    interfaces_ = api.get_resource('/interface')
    interfaces = interfaces_.get()
    form = AddressFrom()
    interfaces_list_ = []
    for item in interfaces:
        if item['type'] != 'pppoe-in':
            interfaces_list_.append((item['name'], item['name']))
    form.fields['interface'].choices = interfaces_list_
    context = {
        'form': form,
        'router': router
    }
    return render(request, 'routers/address/add.html', context)

def plans(request):
    plans = Plan.objects.all()
    context = {
        'plans': plans
    }
    return render(request, 'routers/plans/index.html', context)
