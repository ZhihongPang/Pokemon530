from rest_framework import serializers
from .models import Player,Animal,Entity


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id','username','level','num_animals')

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        # We can expand on this idea later
        # fields = ('id','owner_id','animal_name','animal_type',
        #             'animal_species','photograph_path','health',
        #             'attack','defense','speed')
        # for now, this is the bare minimum required
        fields = ('player_id', 'animal_name', 'photo_path', 'animal_description')

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('entity_name','entity_class','entity_desc',
                    'health','attack','defense','speed')

class InventorySerializer(serializers.Serializer):
    player = PlayerSerializer()
    animals = AnimalSerializer(many=True)