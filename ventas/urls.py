from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ventas.index'),
    path('add/', views.addClient, name='ventas.add.client'),
]
