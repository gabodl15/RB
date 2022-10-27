from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='clients.index'),
    path('create/', views.ClientCreateView.as_view(), name='clients.create'),
    path('show/<int:id>/', views.show, name='clients.show'),
    path('add/profile/<int:id>/', views.addProfile, name="clients.profile.add"),
]
