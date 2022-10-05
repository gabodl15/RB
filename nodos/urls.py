from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='nodos.index'),
    path('show/<int:id>/', views.show, name='nodos.show'),
    path('show/antenna/<str:ip>', views.antenna, name='nodos.show.antenna'),
]
