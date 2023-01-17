from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='administrations.index'),
    path('client/<int:id>/payment/', views.payment, name='administrations.client.payment'),
    path('suspend/not/', views.do_not_suspend, name='administration.suspend.not')
]
