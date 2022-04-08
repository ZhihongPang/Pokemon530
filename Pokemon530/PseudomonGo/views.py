from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .serializer import *
from .models import *


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

class PlayerInventoryViewSet(viewsets.ViewSet):
    """
    A simple API ViewSet for listing the Player and their owned Animals.
    """
    serializer_class = RobotSerializer
    queryset = Robot.objects.all()
    
    @api_view(['GET'])
    def list(self, pk):
        from collections import namedtuple

        Inventory = namedtuple('Inventory', ('player', 'animals'))
        inventory = Inventory(
            player=get_object_or_404(Player, pk=pk),
            animals=Animal.objects.filter(owner_id=pk),
        )
        serializer = InventorySerializer(inventory)
        return JsonResponse(serializer.data)

def battle_system_beta(request):
    if request.method == 'POST':
        pass
    return render(request, 'battle.html', {
        'players': Player.objects.all(),
    })
