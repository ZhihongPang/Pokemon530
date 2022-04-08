from django.db import models


# Create your models here.
class Player(models.Model):
    username = models.CharField(max_length=50)
    level = models.IntegerField()
    num_animals = models.IntegerField()


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


class Robot(models.Model):
    type = models.CharField(max_length=25)
    health = models.FloatField()
    attack = models.FloatField()
    defense = models.FloatField()
    speed = models.FloatField()