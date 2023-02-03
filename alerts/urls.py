from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='alerts.index'),
    path('attending/<int:id>/', views.attending, name='alerts.attending'),
    path('solved/<int:id>/', views.solved, name='alerts.solved'),
    path('delete/<int:id>/', views.delete, name='alerts.delete')
]
