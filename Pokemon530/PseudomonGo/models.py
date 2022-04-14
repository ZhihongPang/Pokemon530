from django.db import models
from django.contrib.auth.models import User
from django_google_maps import fields as map_fields


# Create your models here.
# Player Model linked to the auth_user model
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    level = models.IntegerField(default=1)
    num_animals = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class EntityClass(models.Model):
    class_name = models.CharField(max_length=50)
    class_description = models.CharField(max_length=150)

    def __str__(self):
        return self.class_name


class Entity(models.Model):
    entity_name = models.CharField(max_length=50)
    entity_class = models.ForeignKey(EntityClass, on_delete=models.CASCADE)
    base_atk = models.IntegerField
    Base_def = models.IntegerField
    Base_hp = models.IntegerField
    entity_desc = models.CharField(max_length=150)

    def __str__(self):
        return self.entity_name


class Animal(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    animal_species = models.ForeignKey(Entity, on_delete=models.CASCADE)
    animal_class = models.ForeignKey(EntityClass, on_delete=models.CASCADE, null=True)
    animal_name = models.CharField(max_length=50)
    photograph_path = models.CharField(max_length=100)
    health = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    speed = models.IntegerField()

    def __str__(self):
        return self.animal_name


class StatusCondition(models.Model):
    status_name = models.CharField(max_length=25)

    def __str__(self):
        return self.status_name


class Move(models.Model):
    entity_class = models.ManyToManyField(EntityClass)
    entity = models.ManyToManyField(Entity)
    move_name = models.CharField(max_length=50)
    status_inflicted = models.ForeignKey(StatusCondition, on_delete=models.CASCADE)
    infliction_chance = models.IntegerField
    accuracy = models.IntegerField
    base_damage = models.IntegerField(default=0)
    atk_multiplier = models.FloatField(default=1)
    def_multiplier = models.FloatField(default=1)
    spd_multiplier = models.FloatField(default=1)
    move_description = models.CharField(max_length=150)

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
        default=COMMON,
    )

    item_cost = models.IntegerField
    item_type = models.CharField(max_length=25)
    item_description = models.CharField(max_length=150)

    def __str__(self):
        return self.item_name


class PlayerInventory(models.Model):
    player_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField

    def __str__(self):
        return self 
      
      
# prepares for a widget location
class Rental(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)