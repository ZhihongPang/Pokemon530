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
from django.views.generic.base import TemplateView


'''
Core APIs for standard actions across the app
'''
router = routers.DefaultRouter()
router.register(r'users', views.UserView, 'user')
router.register(r'players', views.PlayerView, 'player')
router.register(r'entity-classes', views.EntityClassView, 'entity-class')
router.register(r'entities', views.EntityView, 'entity')
router.register(r'animals', views.AnimalView, 'animal')
router.register(r'animal-images', views.AnimalImageView, 'animal-image')
router.register(r'status-conditions', views.StatusConditionView, 'status-cond')
router.register(r'moves', views.MoveView, 'move')
router.register(r'items', views.ItemView, 'item')
router.register(r'player-inventories', views.PlayerInventoryView, 'player-inv')
router.register(r'rentals', views.RentalView, 'rental')


urlpatterns = [
    path('api/', include(router.urls)), # For Devs -- Core API routes

    # for creating users and logging them in/out -- DEPRECATED!
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/authenticated-user/', views.AuthenticatedUserView.as_view(), name='authenticated-user'),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),

    # for developer documentation
    path('docs/', views.index, name='home'),

    # home page where the dashboard will be
    path('', TemplateView.as_view(template_name='PseudomonGo/home.html'), name='home'),
    
    # for signups, login, logout, and password resets
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),

    # app pages' routes go here
    path('animals/', views.AnimalUpload, name="Upload"),
    path('battle/', views.battleSystem, name='battle'),
    path("map/", views.map, name="map")
]
