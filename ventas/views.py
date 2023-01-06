from django.shortcuts import render
from clients.forms import ClientForm

# Create your views here.
def index(request):
    context ={

    }
    return render(request, 'ventas/index.html', context)

def addClient(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        print(form.save(commit=False))
    form = ClientForm()
    context = {
        'form': form
    }
    return render(request, 'ventas/add_client.html', context)