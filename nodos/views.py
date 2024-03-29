from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import State, Nodo, CompanyAntenna
import paramiko, json, requests, folium

# FUNCTIONS THAT ARE NOT A VIEW
def ssh_connection(request, antenna):
    host = antenna.ip
    username = antenna.username
    password = antenna.password

    try:
        antenna_connection = paramiko.client.SSHClient()
        antenna_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        antenna_connection.connect(host, username=username, password=password)
        _stdin, _stdout, _stderr = antenna_connection.exec_command('wstalist')
        get_result = _stdout.read().decode()
        antenna_connection.close()
        return get_result

    except paramiko.ssh_exception.AuthenticationException:
        messages.error(request, 'USUARIO O CLAVE INCORRECTOS')

    return redirect(request.META.get('HTTP_REFERER'))


# Create your views here.
def index(request):
    
    states = State.objects.all().values_list('name', flat=True)
    if states:
        # Obtener los datos GeoJSON de los estados de Venezuela
        geoven = "https://raw.githubusercontent.com/wmgeolab/geoBoundaries/a7fd934150a38de07d58f51dc5df51de914c9873/releaseData/gbOpen/VEN/ADM1/geoBoundaries-VEN-ADM1_simplified.geojson"
        response = requests.get(geoven)
        data = response.json()

        # Crear un objeto GeoJSON que contenga los estados de Los Estados
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }

        for feature in data["features"]:
            if feature["properties"]["shapeName"] in states:
                geojson["features"].append(feature)

        m = folium.Map(location=[8.000000, -66.000000], zoom_start=5.5)
        # Agregar la capa de estados al mapa
        folium.GeoJson(geojson).add_to(m)
        map = m.get_root().render()
    else:
        map = None

    nodos = Nodo.objects.all()
    context = {
        'nodos': nodos,
        'states': states,
        'map': map,
    }
    return render(request, 'nodos/index.html', context)

def show(request, id):
    nodo = Nodo.objects.get(id=id)
    antennas = nodo.companyantenna_set.filter(nodo=id)
    return render(request, 'nodos/show.html', {'nodo':nodo, 'antennas': antennas})

def antenna(request, ip):
    antenna = CompanyAntenna.objects.filter(ip=ip).first()
    get_station_info = ssh_connection(request, antenna)
    if isinstance(get_station_info, HttpResponseRedirect):
        return get_station_info

    details = json.loads(get_station_info)
    context = {
        'details': details,
        'antenna': antenna
    }
    return render(request, 'nodos/antenna.html', context)
