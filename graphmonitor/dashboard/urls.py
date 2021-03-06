"""graphmonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('switch/add/', views.SwitchCreateView.as_view(), name='add-switch'),
    path('switch/<int:pk>/', views.SwitchUpdateView.as_view(), name='update-switch'),
    path('command/add/', views.CommandCreateView.as_view(), name='add-command'),
    path('command/<int:pk>/', views.CommandUpdateView.as_view(), name='update-command'),
    path('device/add/', views.DeviceCreateView.as_view(), name='add-device'),
    path('device/<int:pk>/', views.DeviceUpdateView.as_view(), name='update-device'),
    path('graphs/all/', views.all_graphs, name='all-graphs'),
    path('switch/<int:pk>/commands/', views.get_switch_commands, name='get-switch-commands'),
    path('switch/<int:pk>/delete/', views.delete_switch, name='delete-switch'),
    path('device/<int:pk>/delete/', views.delete_device, name='delete-device'),
    path('switch/<int:pk>/start/', views.start_switch, name='start-switch'),
    path('switch/<int:pk>/stop/', views.stop_switch, name='stop-switch'),
    path('device/<int:pk>/data/delete/', views.delete_device_data, name='delete-device-data')

    #path('switch/<int:pk>/delete/', views.SwitchDeleteView.as_view(), name='delete-switch'),
] # path('add-series', views.add_series, name='add_series')

                    # from homepage.consumers import UpdateConsumer
ws_urlpatterns = [] # path('update-series', UpdateConsumer.as_asgi())
