from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='text_messages.index'),
    path('send/', views.send, name='text_messages.send'),
]