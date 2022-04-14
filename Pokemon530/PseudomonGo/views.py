from pdb import lasti2lineno
from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .serializer import *
from .models import *
from .forms import ImageForm


# Create your views here.
class PlayerView(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

# class AnimalView(viewsets.ModelViewSet):
#     serializer_class = AnimalSerializer
#     queryset = Animal.objects.all()

class EntityView(viewsets.ModelViewSet):
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()

class PlayerInventoryViewSet(viewsets.ViewSet):
    """
    A simple API ViewSet for listing the Player and their owned Animals.
    """
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()
    
    @api_view(['GET'])
    def list(self, pk):
        from collections import namedtuple

        Inventory = namedtuple('Inventory', ('player', 'animals'))
        inventory = Inventory(
            player = get_object_or_404(Player, pk=pk),
            animals = Animal.objects.filter(owner_id=pk),
        )
        serializer = InventorySerializer(inventory)
        return JsonResponse(serializer.data)

def BattleSystem(request, pk):
    return render(request, 'battle.html', {
        'player': get_object_or_404(Player, pk=pk).username,
        'animals': Animal.objects.filter(owner_id=pk),
        'entities': Entity.objects.all()
    })

def AnimalUpload(request):    
    last_image = AnimalImage.objects.order_by('-pub_date')[:5]
    # image_file = last_image.image_file if last_image else None
    form = ImageForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        form.save()
        
    context= {
                'last_animal': last_image,
                # 'image_file': image_file,
                'form': form,
            }
      
    return render(request, 'images.html', context)

def Index(request):
    return render(request, 'index.html')
