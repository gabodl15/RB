from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import Inspect, Material, Install, Log, Support
from .forms import FeasibleOrNotFeasibleForm, MaterialFiberForm, MaterialWirelessForm
from .sheet_pdf import Pdf
from clients.models import Client, Profile
from clients.functions import RouterProfile
from routers.models import Router, Plan
from routers.functions import Connection
from ventas.models import Inspection, FeasibleOrNotFeasible as VentasFeasibleOrNotFeasible

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import io

# Create your views here.
def index(request):
    missing_inspect = Inspect.objects.filter(realized='NOT')
    missing_install = Install.objects.filter(realized='NOT')
    missing_support = Support.objects.filter(realized='NOT')
    context = {
        'missing_inspect': missing_inspect,
        'missing_install': missing_install,
    }
    return render(request, 'supports/index.html', context)

def show(request, id):
    installation = Install.objects.get(id=id)
    client = installation.inspect.inspect.client
    material = installation.inspect.material
    routers = Router.objects.all().order_by('name')
    context = {
        'installation': installation,
        'client': client,
        'material':material,
        'routers': routers
    }
    return render(request, 'supports/show.html', context)

def installation_realized(request, id):
    installation = Install.objects.get(id=id)
    installation.realized = 'YES'
    installation.save()
    messages.success(request, 'SE HA REALIZADO LA INSTALACIÓN')
    return redirect('supports.index')

def inspection_show(request, id):
    support_inspection = Inspect.objects.get(id=id)
    if request.method == 'POST':
        """ VALIDAMOS QUE EL FOR SEA VALIDO """
        form_feasible = FeasibleOrNotFeasibleForm(request.POST)

        if form_feasible.is_valid():
            """ OBTENEMOS EL OBJECTO SIN GUARDARLO """
            support_feasible = form_feasible.save(commit=False)

            """ EN EL CASO DE QUE SEA FACTIBLE """
            if 'NOT' not in support_feasible.feasible:
                material = MaterialFiberForm(request.POST) if support_inspection.inspect.inspection_type == "OF" else MaterialWirelessForm(request.POST)
                if material.is_valid():
                    """ CREAR LISTA DE MATERIALES """
                    material.save()
                else:
                    messages.error(request, 'FORMULARIO DE MATERIALES NO VALIDO')
                    return redirect('supports.inspection.update', id=id)
            """ GUARDO EL OBJECTO UNA VEZ VERIFICADO AMBOS FORMUARIOS """
            support_feasible.save()

            ventas_inspection = Inspection.objects.get(id=support_inspection.inspect_id)
            ventas_inspection.inspection = 'YES'
            ventas_inspection.save()

            """ INSPECCION REALIZADA """
            support_inspection.realized = 'YES'
            support_inspection.save()
            """ REGISTRANDO EN EL LOG QUE SE REALIZÓ LA INSPECCION """
            support_log = Log(
                            user=request.user,
                            action='Inspección Realizada',
                            message='La inspección para el cliente {} fue realizada'.format(support_inspection)
                            )
            support_log.save()

            """ FACTIBLE O NO EN VENTAS """
            ventas_feasible = VentasFeasibleOrNotFeasible()
            ventas_feasible.inspection = ventas_inspection
            ventas_feasible.feasible = support_feasible.feasible
            ventas_feasible.comment = support_feasible.comment
            ventas_feasible.save()
        else:
            messages.error(request, 'FORMULARIO NO VALIDO')
            return redirect('supports.inspection.update', id=id)

        return redirect('supports.index')
    client = support_inspection.inspect.client
    form = FeasibleOrNotFeasibleForm(initial={'inspect': support_inspection})
    material_form = MaterialFiberForm(initial={'inspect': support_inspection}) if support_inspection.inspect.inspection_type == "OF" else MaterialWirelessForm(initial={'inspect': support_inspection})
    context ={
        'client': client,
        'form': form,
        'inspect': support_inspection,
        'material_form': material_form,
    }
    return render(request, 'supports/inspection_show.html', context)

def support_print(request, support, id):
    if support == 'installations':
        obj = Install.objects.get(id=id)
        client_id = obj.inspect.inspect.client.id
    if support == 'inspections':
        obj = Inspect.objects.get(id=id)
        client_id = obj.inspect.client.id
    client = Client.objects.get(id=client_id)
    media = settings.MEDIA_URL

    sheet = Pdf(obj, client, support)
    saved_sheet = sheet.create_sheet()

    support_sheet = media + saved_sheet

    data = {
            'support_sheet':support_sheet
    }
    return JsonResponse(data)

def support_add(request):
    pass

def create_ppp(request):
    profile = RouterProfile()
    if profile.create(request):
        messages.success(request, 'USUARIO CREADO SATISFACTORIAMENTE')
        return redirect('supports.index')
    messages.error(request, 'HUBO UN PROBLEMA AL CREAR EL USUARIO')
    return redirect('index')

def support_ppp_conf_ajax(request, name, id):
    router = Router.objects.get(id=id)
    connection = Connection(router)
    username = name

    if not connection.active:
        return JsonResponse({'success': False})

    # ORDENAR LA LISTA DE PERFILES POR LA CONTRASEÑA
    profile_list = Profile.objects.filter(router=router.id)
    if profile_list:
        # profile_dict = {profile.id: profile for profile in profile_list}
        sorted_profile_list = sorted(profile_list, key=lambda x: x.password)

        # OBTENER EL ÚLTIMO ELEMENTO DE LA LISTA ORDENADA.
        last_profile = sorted_profile_list[-1]

        # OBTENER LA CONTRASEÑA DEL ULTIMO ELEMENTO.
        last_password = last_profile.password

        # ASIGNAMOS NUEVA CONTRASEÑA PARA EL PERFIL NUEVO.
        assing_password = int(last_password) + 1
    else:
        assing_password = '0001'

    plans_mk = connection.query('/ppp/profile')
    plans_mk_list = [plan['name'] for plan in plans_mk]
    plans = Plan.objects.filter(name__in=plans_mk_list)
    plans_list = []
    if plans:
        for plan in plans:
            plans_list.append({'id': plan.id, 'name': plan.name})
    else:
        plans_list.append({'id':0, 'name':0})
    counter = 0
    while True:
        search = connection.name_query('/ppp/secret', username)

        if not search:
            break
        counter += 1
        username = name + str(counter)

    data = {
        'success': True,
        'ppp':username,
        'password': assing_password,
        'plans':plans_list
        }
    return JsonResponse(data)
