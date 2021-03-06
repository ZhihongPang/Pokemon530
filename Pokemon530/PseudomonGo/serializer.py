from rest_framework import serializers
from .models import *


'''
Basic serializers for all models in .models
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # for post requests when creating a user via a login page
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = User(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class AnimalSerializer(serializers.ModelSerializer):
    health = serializers.ReadOnlyField()
    attack = serializers.ReadOnlyField()
    defense = serializers.ReadOnlyField()
    speed = serializers.ReadOnlyField()
    class Meta:
        model = Animal
        fields = '__all__'

class StatusConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusCondition
        fields = '__all__'

class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = '__all__'

class EntitySerializer(serializers.ModelSerializer):
    moves = MoveSerializer(read_only=True, many=True)

    class Meta:
        model = Entity
        fields = '__all__'

class EntityClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityClass
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class PlayerInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerInventory
        fields = '__all__'

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'