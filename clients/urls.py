from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='clients.index'),
    path('show/<int:id>/', views.show, name='clients.show'),
]
