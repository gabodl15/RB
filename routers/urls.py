from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='routers.index'),
    path('create/', views.create, name='routers.create'),
    path('edit/<int:id>/', views.edit, name='routers.edit'),
    path('update/<int:router>/', views.update, name='routers.update'),
    path('show/<int:router>/', views.show, name='routers.show'),
    path('store/', views.store, name='routers.store'),
    path('delete/<int:router>/', views.delete, name='routers.delete'),
    path('queue/add/', views.addQueue, name='routers.queue.add'),
    path('ppp/add/<int:router>', views.addPpp, name='routers.ppp.add')
]
