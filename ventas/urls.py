from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ventas.index'),
    path('add/<int:id>', views.addInspection, name='ventas.inspection.add'),
    path('inspection/reulst/', views.inspectionResult, name='ventas.inspection.result'),
    path('inspection/show/', views.showInspection, name='ventas.inspection.show'),
    path('inspection/update/<int:id>/', views.updateInspection, name='ventas.inspection.update'),
    path('inspection/inform/<int:id>/', views.informInspection, name='ventas.inspection.inform'),
    path('inspection/informed/', views.informedInspection, name='ventas.inspection.informed'),
]
