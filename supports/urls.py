from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='supports.index'),
    path('inspection/show/<int:id>/', views.inspection_show, name='supports.inspection.update'),
    path('installation/show/<int:id>', views.show, name='supports.installation.show'),
    path('<str:support>/print/order/<int:id>', views.support_print, name='supports.print')
]