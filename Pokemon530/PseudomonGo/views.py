from django.shortcuts import render
from rest_framework import viewsets
from .serializer import PlayerSerializer, AnimalSerializer, RobotSerializer
from .models import Player, Animal, Robot


# Create your views here.
class PlayerView(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

class AnimalView(viewsets.ModelViewSet):
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()

class RobotView(viewsets.ModelViewSet):
    serializer_class = RobotSerializer
    queryset = Robot.objects.all()

def battle(request):
    import requests

    animals = requests.get('http://127.0.0.1:8000/api/animals/?format=json')
    robots = requests.get('http://127.0.0.1:8000/api/robots/?format=json')
    return render(request, 'battle.html', {
        'animals':animals, 'robots':robots
    })