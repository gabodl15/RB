from django.shortcuts import render
from django.contrib import messages
from .models import Client
from .forms import ClientForm
def index(request):
    clients = Client.objects.all()
    return render(request, 'clients/index.html', {'clients': clients})

def create(request):
    form = ClientForm
    return render(request, 'clients/create.html', {'form': form})

def store(request):
    if request.method == 'POST':
        name = request.POST['name']
        last_name = request.POST['last_name']
        dni = request.POST['dni']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        client = Client(name=name,
                        last_name=last_name,
                        email=email,
                        dni=dni,
                        phone=phone,
                        address=address,
                        )
        client.save()
        messages.success(request, 'CLIENTE REGISTRADO CON EXITO')
    return render(request, 'clients/index.html', {})
def show(request, id):
    client = Client.objects.get(id=id)
    return render(request, 'clients/show.html', {'client': client})