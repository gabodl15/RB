from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='routers.index'),
    path('show/<int:id>/', views.show, name='routers.show'),
    path('queue/add/<int:id>/', views.addQueue, name='routers.queue.add'),
    path('ppp/add/<int:id>/', views.addPpp, name='routers.ppp.add'),
    path('address/add/<int:id>', views.addAddress, name='routers.address.add'),
    path('plans/', views.plans, name='routers.plans.index'),
]
