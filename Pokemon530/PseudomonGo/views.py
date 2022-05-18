from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ParseError
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from .serializer import *
from .models import *
from .forms import UploadForm, RateAnimalForm, RemoveForm
from .admin import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
import os


'''
Basic Model API Views for all models in .models to be accessed in /api
'''
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class PlayerView(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

class EntityClassView(viewsets.ModelViewSet):
    serializer_class = EntityClassSerializer
    queryset = EntityClass.objects.all()

class EntityView(viewsets.ModelViewSet):
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()

class AnimalView(viewsets.ModelViewSet):
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()

class StatusConditionView(viewsets.ModelViewSet):
    serializer_class = StatusConditionSerializer
    queryset = StatusCondition.objects.all()

class MoveView(viewsets.ModelViewSet):
    serializer_class = MoveSerializer
    queryset = Move.objects.all()

class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class PlayerInventoryView(viewsets.ModelViewSet):
    serializer_class = PlayerInventorySerializer
    queryset = PlayerInventory.objects.all()

class RentalView(viewsets.ModelViewSet):
    serializer_class = RentalSerializer
    queryset = Rental.objects.all()

'''
Other API views go here
'''

'''
API for registering a user

Sample JSON format for POST
{
    "email":"your_email@email.com",
    "username":"your_name",
    "password":"your_password"
}
'''
class RegisterView(APIView):
    permission_classes = [AllowAny] # creating users is publicly available

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

'''
API for logging in

Sample JSON format for POST
{
    "username":"your_name",
    "password":"your_password"
}
'''
class LoginView(APIView):
    permission_classes = [AllowAny] # let logins be publicly available

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            raise ParseError()
        # do user auth
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        if user is None:
            raise AuthenticationFailed('User not found')
        return Response(data={'login': 'success'})

'''
API for checking if user is logged in

ONLY GET requests allowed, sample JSON payload
{
    "logged in as":"user_name"
}
'''
class AuthenticatedUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        response = Response()
        if request.user.is_authenticated:
            response.data = {'logged in as': request.user.username}
            return response
        raise AuthenticationFailed('Not logged in')

'''
API for logging out
'''
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response(data={'status': 'logout success'})

'''
User sign up view
'''
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


'''
Custom views go here
'''
@login_required(login_url='/accounts/login/')
def battleSystem(request):
    robot_class = EntityClass.objects.filter(class_name="Robot")
    robots = {}
    if robot_class:
        robots = Entity.objects.filter(entity_class=robot_class[0])
    auth = request.user
    return render(request, 'PseudomonGo/battle.html', {
        'player': request.user,
        'animals': Animal.objects.filter(player=request.user),
        'robots': robots,
        'moves': Move.objects.all().values(),
        'items': PlayerInventory.objects.filter(player=request.user)
    })

# animal functions
@login_required(login_url='/accounts/login/')
def animalUpload(request):
    player_animals = Animal.objects.filter(player=request.user)
    form = UploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        player = Player.objects.get(user=request.user)
        player.num_animals += 1
        player.save()

        # Why does Django want me to make this jank duct tape code
        # just so I can use a different foreign key for the user field??

        candidate = form.save(commit=False)
        candidate.player = User.objects.get(username=request.user.username)  # use your own profile here

        moves = Move.objects.all()
        if moves and len(moves) >= 4:
            candidate.move1 = Move.objects.all()[0]
            candidate.move2 = Move.objects.all()[1]
            candidate.move3 = Move.objects.all()[2]
            candidate.move4 = Move.objects.all()[3]

        candidate.save()

        return HttpResponseRedirect("/upload-success")
    context = {
                'player_animals': player_animals,
                'form': form,
            }
    return render(request, 'PseudomonGo/upload.html', context)

@login_required(login_url='/accounts/login/')
def animalRemove(request):
    player_animals = Animal.objects.filter(player=request.user)
    form = RemoveForm(request.POST or None)
    if form.is_valid():
        deleted_animal = player_animals.get(animal_name=form.cleaned_data['animal_name'])
        os.remove(os.path.join(settings.MEDIA_ROOT, 'images/'+deleted_animal.filename()))
        player = Player.objects.get(user=request.user)
        player.num_animals -= 1
        player.save()
        deleted_animal.delete()
    context = {
                'player_animals': player_animals
            }
    return render(request, 'PseudomonGo/remove.html', context)

@login_required(login_url='/accounts/login/')
def animalView(request):
    player_animals = Animal.objects.filter(player=request.user)
    context = {
        'player': request.user,
        'player_animals': player_animals
    }
    return render(request, 'PseudomonGo/view.html', context)

@login_required(login_url='/accounts/login/')
def animals(request):
    all_animals = Animal.objects.all()
    context = {
                'all_animals': all_animals
            }
    return render(request, 'PseudomonGo/animals.html', context)

@login_required(login_url='/accounts/login/')
def animalReview(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    if request.method == "POST":
        form = RateAnimalForm(request.POST)
        if form.is_valid():
            rating = Rating(animal=animal, rating=form.cleaned_data["rating"])
            rating.save()
    else:
        form = RateAnimalForm()
    context = {"animal": animal, "form": form}
    return render(request, "PseudomonGo/review.html", context)

""" def index(request):
    return render(request, 'PseudomonGo/index.html') """


# calls map html to load
@login_required(login_url='/accounts/login/')
def map(request):
    return render(request, 'PseudomonGo/map.html')


""" # calls map html to load
def dash(request):
    return render(request, 'PseudomonGo/dash.html') """

@login_required(login_url='/accounts/login/')
def profile(request):
    return render(request, 'PseudomonGo/profile.html',{
     'player': Player.objects.filter(user=request.user).first()
    })

'''
main homepage
'''
@login_required(login_url='/accounts/login/')
def home(request):

    # get four most recent animals owned by player
    last_four = Animal.objects.filter(player=request.user).order_by('-id')[:4]
    last_four_in_ascending_order = reversed(last_four)

    return render(request, 'PseudomonGo/home.html', {
        'player_animals': last_four_in_ascending_order
    })
