from rest_framework import serializers
from .models import Player,Animal,Robot


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id','username','level','num_animals')

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ('id','owner_id','animal_name','animal_type',
                    'animal_species','photograph_path','health',
                    'attack','defense','speed')

class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ('id','robot_type','health','attack','defense','speed')

class InventorySerializer(serializers.Serializer):
    player = PlayerSerializer()
    animals = AnimalSerializer(many=True)