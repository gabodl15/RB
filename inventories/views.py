from django.shortcuts import render
from .models import Inventory

# Create your views here.
def index(request):
    inventories = Inventory.objects.all()
    context = {
        'inventories': inventories
    }
    return render(request, 'inventories/index.html', context)