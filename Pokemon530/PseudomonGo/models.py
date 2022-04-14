from django.db import models
from django_google_maps import fields as map_fields

# Create your models here.
class Player(models.Model):
    username = models.CharField(max_length=50)
    level = models.IntegerField()
    num_animals = models.IntegerField()

    def __str__(self):
        return self.username


class Animal(models.Model):
    owner_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    animal_name = models.CharField(max_length=50)
    animal_type = models.CharField(max_length=50)
    animal_species = models.CharField(max_length=50)
    photograph_path = models.CharField(max_length=100)
    health = models.FloatField()
    attack = models.FloatField()
    defense = models.FloatField()
    speed = models.FloatField()

    def __str__(self):
        return self.animal_name


class Robot(models.Model):
    robot_type = models.CharField(max_length=25)
    health = models.FloatField()
    attack = models.FloatField()
    defense = models.FloatField()
    speed = models.FloatField()

    def __str__(self):
        return self.robot_type

# prepares for a widget location
class Rental(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)