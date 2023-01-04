from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='users.profile'),
    path('configurations/', views.configuration, name='users.configurations'),
    path('change/password/', views.changePassword, name='users.change.password'),
]
