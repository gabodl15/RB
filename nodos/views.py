from django.shortcuts import render
from .models import Nodo, CompanyAntenna
import paramiko, json

# FUNCTIONS THAT ARE NOT A VIEW
def ssh_connection(antenna):
    host = antenna.ip
    username = antenna.username
    password = antenna.password

    antenna_connection = paramiko.client.SSHClient()
    antenna_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    antenna_connection.connect(host, username=username, password=password)
    _stdin, _stdout, _stderr = antenna_connection.exec_command('wstalist')
    get_result = _stdout.read().decode()
    antenna_connection.close()

    return get_result

# Create your views here.
def index(request):
    nodos = Nodo.objects.all()
    return render(request, 'nodos/index.html', {'nodos': nodos})

def show(request, id):
    nodo = Nodo.objects.get(id=id)
    antennas = nodo.companyantenna_set.filter(nodo=id)
    return render(request, 'nodos/show.html', {'nodo':nodo, 'antennas': antennas})

def antenna(request, ip):
    antenna = CompanyAntenna.objects.filter(ip=ip).first()
    get_station_info = ssh_connection(antenna)
    details= json.loads(get_station_info)
    return render(request, 'nodos/antenna.html',{'details': details})