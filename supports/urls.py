from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='supports.index'),
    path('inspection/show/<int:id>/', views.inspection_show, name='supports.inspection.update'),
    path('inspection/delete/<int:id>/', views.inspection_delete, name='supports.inspection.delete'),
    path('installation/show/<int:id>/', views.installation_show, name='supports.installation.show'),
    path('installation/delete/<int:id>/', views.installation_delete, name='supports.installation.delete'),
    path('installation/realized/<int:id>/', views.installation_realized, name='supports.intallation.realized'),
    path('support/add/<int:id>/', views.support_add, name='supports.add.support'),
    path('support/delete/<int:id>/', views.support_delete, name='supports.support.delete'),
    path('support/update/<int:id>/', views.support_update, name='supports.update.support'),
    path('<str:support>/print/order/<int:id>/', views.support_print, name='supports.print'),
    path('ppp/<str:name>/conf/ajax/router/<int:id>/', views.support_ppp_conf_ajax, name='supports.ppp.conf.ajax'),
    path('ppp/create/', views.create_ppp, name='supports.create.ppp')
]
