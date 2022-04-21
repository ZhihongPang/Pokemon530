from pdb import lasti2lineno
from django import views
from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .serializer import *
from .models import *
from .forms import ImageForm
from .admin import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from Pokemon530 import settings


'''
Basic views for all models in .models to be accessed in /api
'''
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class PlayerView(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    permission_classes = [IsAuthenticated]

class EntityClassView(viewsets.ModelViewSet):
    serializer_class = EntityClassSerializer
    queryset = EntityClass.objects.all()

class EntityView(viewsets.ModelViewSet):
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()

class AnimalView(viewsets.ModelViewSet):
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()
    permission_classes = [IsAuthenticated]

class AnimalImageView(viewsets.ModelViewSet):
    serializer_class = AnimalImageSerializer
    queryset = AnimalImage.objects.all()
    permission_classes = [IsAuthenticated]

class StatusConditionView(viewsets.ModelViewSet):
    serializer_class = StatusConditionSerializer
    queryset = StatusCondition.objects.all()
    permission_classes = [IsAuthenticated]

class MoveView(viewsets.ModelViewSet):
    serializer_class = MoveSerializer
    queryset = Move.objects.all()

class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]

class PlayerInventoryView(viewsets.ModelViewSet):
    serializer_class = PlayerInventorySerializer
    queryset = PlayerInventory.objects.all()
    permission_classes = [IsAuthenticated]

class RentalView(viewsets.ModelViewSet):
    serializer_class = RentalSerializer
    queryset = Rental.objects.all()


# custom views go here

def battleSystem(request):
    return render(request, 'battle.html', {
        'animals': Animal.objects.all(),
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

def index(request):
    return render(request, 'index.html')

# calls map html to load
def map(request):
    return render(request, 'map.html')
