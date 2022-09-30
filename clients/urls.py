from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='clients.index'),
    path('create/', views.create, name='clients.create'),
    path('show/<int:id>/', views.show, name='clients.show'),
    path('store/', views.store, name='clients.store')
]
