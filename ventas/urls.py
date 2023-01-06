from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ventas.index'),
    path('add/<int:id>', views.addInspection, name='ventas.inspection.add'),
]
