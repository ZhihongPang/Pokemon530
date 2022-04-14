"""Pokemon530 URL Configuration

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
from django.urls import path, include
from rest_framework import routers
from PseudomonGo import views

router = routers.DefaultRouter()
# router.register(r'players', views.PlayerView, 'player')
# router.register(r'animals', views.AnimalView, 'animal')
# router.register(r'entities', views.EntityView, 'entity')

urlpatterns = [
    path('', views.Index, name='home'),
    # path('api/', include(router.urls)),
    path('animals/', views.AnimalUpload, name="Upload"),
    path('api/players/<int:pk>/inventory', views.PlayerInventoryViewSet.list, name='player inventory'),
    path('battle/<int:pk>', views.BattleSystem, name='battle')
]
