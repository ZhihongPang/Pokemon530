from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.db.models import Avg
from django_google_maps import fields as map_fields


# Create your models here.
# Player Model linked to the auth_user model
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    experience = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    num_animals = models.IntegerField(default=0)
    money = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class EntityClass(models.Model):
    class_name = models.CharField(max_length=50)
    class_description = models.CharField(max_length=500)

    def __str__(self):
        return self.class_name


class Entity(models.Model):
    entity_name = models.CharField(max_length=50)
    entity_class = models.ForeignKey(EntityClass, on_delete=models.CASCADE)
    base_atk = models.IntegerField(default=75)
    base_def = models.IntegerField(default=50)
    base_hp = models.IntegerField(default=100)
    base_spd = models.IntegerField(default=50)
    entity_desc = models.CharField(max_length=500)

    def __str__(self):
        return self.entity_name


class Animal(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    animal_name = models.CharField(max_length=50)
    animal_description = models.TextField(max_length=500)
    animal_location = models.CharField(max_length=50, verbose_name="Sighted Location")
    photo_path = models.FileField(upload_to='images/', null=True, verbose_name="", default=None)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    animal_species = models.ForeignKey(Entity, on_delete=models.CASCADE, default=1)
    animal_class = models.ForeignKey(EntityClass, on_delete=models.CASCADE, default=1)
    health = models.IntegerField(default=100)
    attack = models.IntegerField(default=1)
    defense = models.IntegerField(default=1)
    speed = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)

    move1 = models.ForeignKey("Move", on_delete=models.CASCADE, default=None, null=True,
                              related_name='move1',blank=True)
    move2 = models.ForeignKey("Move", on_delete=models.CASCADE, default=None, null=True,
                              related_name='move2', blank=True)
    move3 = models.ForeignKey("Move", on_delete=models.CASCADE, default=None, null=True,
                              related_name='move3', blank=True)
    move4 = models.ForeignKey("Move", on_delete=models.CASCADE, default=None, null=True,
                              related_name='move4', blank=True)


    # the default string of the animal is the animal name + its image path

    def __str__(self):
        return self.animal_name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    # use this function if you want just the name of the animal
    def has_animal_name(self):
        return self.animal_name + ": " + str(self.photo_path)
        
    def has_animal_description(self):
        return self.animal_description
    
    def avg_rating(self):
        avg_rating = self.rating_set.all().aggregate(Avg("rating"))["rating__avg"]
        if not avg_rating:
            return "not rated"
        else:
            return round(avg_rating, 2)


class Rating(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    rating = models.IntegerField()


class StatusCondition(models.Model):
    status_name = models.CharField(max_length=25)

    def __str__(self):
        return self.status_name


class Move(models.Model):
    entity_class = models.ManyToManyField(EntityClass, default=None, blank=True)
    entity = models.ManyToManyField(Entity)
    move_name = models.CharField(max_length=50)
    status_inflicted = models.ForeignKey(StatusCondition, on_delete=models.CASCADE,
                                         null=True, default=None, blank=True)
    infliction_chance = models.IntegerField(default=100)
    accuracy = models.IntegerField(default=100)
    base_damage = models.IntegerField(default=0)
    atk_multiplier = models.FloatField(default=1)
    def_multiplier = models.FloatField(default=1)
    spd_multiplier = models.FloatField(default=1)
    move_description = models.CharField(max_length=500)

    ATTACK = 'A'
    STATUS = 'S'
    MOVE_TYPE = [
        (ATTACK, 'Attack'),
        (STATUS, 'Status'),
    ]
    move_type = models.CharField(
        max_length=2,
        choices=MOVE_TYPE,
        default=ATTACK,
    )

    SELF = 'S'
    OPPONENT = 'O'
    TARGET = [
        (SELF, 'Self'),
        (OPPONENT, 'Opponent'),
    ]
    target = models.CharField(
        max_length=2,
        choices=TARGET,
        default=OPPONENT,
    )

    def __str__(self):
        return self.move_name


class Item(models.Model):
    item_name = models.CharField(max_length=25)

    COMMON = 'C'
    UNCOMMON = 'U'
    RARE = 'R'
    EPIC = 'E'
    LEGENDARY = 'L'
    ITEM_RARITY = [
        (COMMON, 'Common'),
        (UNCOMMON, 'Uncommon'),
        (RARE, 'Rare'),
        (EPIC, 'Epic'),
        (LEGENDARY, 'Legendary'),
    ]
    item_rarity = models.CharField(
        max_length=2,
        choices=ITEM_RARITY,
        default=COMMON,)
    healing = models.IntegerField(default=0)
    ATK = 'AT'
    DEF = 'D'
    SPD = 'S'
    NONE = 'N'
    ALL = 'AL'
    STAT_BUFFED = [
        (ATK, 'Attack'),
        (DEF, 'Defense'),
        (SPD, 'Speed'),
        (NONE, 'None'),
        (ALL, 'ALL')
    ]
    stat_buffed = models.CharField(
        max_length=4,
        choices=STAT_BUFFED,
        default=NONE)
    buff_multiplier = models.IntegerField(default=1)
    status_cured = models.CharField(max_length=25, default='none')
    item_cost = models.IntegerField(default=0)
    item_type = models.CharField(max_length=25)
    item_description = models.CharField(max_length=500)

    def __str__(self):
        return self.item_name


class PlayerInventory(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.player.username+"-"+self.item.item_name
      
      
# prepares for a widget location
class Rental(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)