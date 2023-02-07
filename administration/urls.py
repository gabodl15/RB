from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='administrations.index'),
    path('client/<int:id>/payment/', views.payment, name='administrations.client.payment'),
    path('suspend/not/', views.do_not_suspend, name='administration.suspend.not'),
    path('suspend/not/delete/<int:id>/', views.do_not_suspend_delete, name='administrations.suspend.not.delete'),
    path('debts/', views.debts, name='administrations.clients.debts'),
    path('debts/delete/<int:id>/', views.debts_delete, name='administrations.clients.debt.delete'),
    path('payment/support/<int:id>/', views.payment_support, name='administrations.clients.payment.support'),
]
