from pdb import lasti2lineno
from django import views
from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

import jwt, datetime

from .serializer import *
from .models import *
from .forms import ImageForm
from .admin import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from Pokemon530 import settings


'''
Basic Model API Views for all models in .models to be accessed in /api
'''
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

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

'''
Other API views go here
'''

# api for registering a user
class RegisterView(APIView):
    permission_classes = [AllowAny] # creating users is publicly available

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# api for logging in
class LoginView(APIView):
    permission_classes = [AllowAny] # let logins be publicly available

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        # set cookie properties for token
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='pseudomongo_jwt', value=token, httponly=True)
        response.data = {
            'pseudomongo_jwt': token
        }
        return response

# api for checking if user is logged in
class AuthenticatedUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.COOKIES.get('pseudomongo_jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        data = serializer.data
        data.update({
            'status': 'login success'
        })
        return Response(data)

# api for deleeting the cookie -> logs out curr user
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response()
        response.delete_cookie('pseudomongo_jwt')
        response.data = {
            'message': 'success'
        }
        return response

'''
Custom views go here
'''
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
