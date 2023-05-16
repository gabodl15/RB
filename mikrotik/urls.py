"""mikrotik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls')),
    path('inventories/', include('inventories.urls')),
    path('nodos/', include('nodos.urls')),
    path('routers/', include('routers.urls')),
    path('users/', include('users.urls')),
    path('administration/', include('administration.urls')),
    path('alerts/', include('alerts.urls')),
    path('ventas/', include('ventas.urls')),
    path('supports/', include('supports.urls')),
    path('text_messages/', include('text_messages.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)