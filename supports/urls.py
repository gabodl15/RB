from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='supports.index'),
    path('inspection/update/<int:id>/', views.updateInspection, name='supports.inspection.update')
]