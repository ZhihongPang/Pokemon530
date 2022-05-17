import datetime

from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from PseudomonGo.models import Animal, EntityClass, Entity

## Tests for Animal Upload ###
class AnimalModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", username="testUser", password="password")
        self.user.save()
        self.C = Client()
        self.animal = Animal()
        enc = EntityClass.objects.create(class_name="Foo", class_description="Bar")
        Entity.objects.create(entity_name="Foo", entity_class=enc) 

    # if you failed any of these then check AnimalImage in models to see if database fields have been initialized correctly
    def test_animal_pub_time(self):
        self.assertIs(self.animal.was_published_recently(), True)
    def test_animal_name(self):
        self.animal.animal_name = "Horse"
        self.assertIs(self.animal.animal_name, "Horse")
    def test_animal_description(self):
        self.animal.animal_description = "This is a horse, trust me bro"
        self.assertIs(self.animal.has_animal_description(), "This is a horse, trust me bro")
    def test_animal_location(self):
        self.animal.animal_location = "UMBC"
        self.assertIs(self.animal.has_animal_location(), "UMBC")
    def test_animal_species(self):
        self.assertNotEqual(self.animal.has_animal_species, True, "This is a foreignkey, should not be connected to anything")
    def test_animal_class(self):
        self.assertNotEqual(self.animal.has_animal_class(), True, "This is a foreignkey, should not be connected to anything")
    def test_animal_rating(self):
        self.assertEqual(self.animal.avg_rating(), "not rated", "Default animals should have no ratings")

    # if you failed this test, then there might be ghost images attached to newly initialized animals
    def test_animal_image(self):
        self.assertNotEqual(self.animal.photo_path, True)
    
    # tests to see if the animal upload is correctly reflected in the database
    def test_animal_upload_name(self):
        self.animal.animal_name = "Horse"
        self.animal.save()
        animal_from_database = Animal.objects.last() # the last entry to the databse should be made by the test case
        self.assertEqual(animal_from_database.animal_name, self.animal.animal_name)
    def test_animal_upload_description(self):
        self.animal.animal_description = "This is a horse, trust me bro"
        self.animal.save()
        animal_from_database = Animal.objects.last()
        self.assertEqual(animal_from_database.animal_description, self.animal.animal_description)
    def test_animal_upload_photo_path(self):
        self.animal.photo_path = "images/download.jpg"
        self.animal.save()
        animal_from_database = Animal.objects.last()
        self.assertEqual(animal_from_database.photo_path, self.animal.photo_path)
    def test_animal_upload_location(self):
        self.animal.animal_location = "UMBC"
        self.animal.save()
        animal_from_database = Animal.objects.last()
        self.assertEqual(animal_from_database.animal_location, self.animal.animal_location)
    def test_animal_upload_rating(self):
        self.animal.save()
        animal_from_database = Animal.objects.last()
        self.assertEqual(animal_from_database.avg_rating(), "not rated", "Default should be not rated")
    def test_animal_upload_stats(self):
        self.animal.save()
        animal_from_database = Animal.objects.last()
        self.assertEqual(animal_from_database.health, 13, "default health is 100")
        self.assertEqual(animal_from_database.attack, 6, "default attack is 1")
        self.assertEqual(animal_from_database.defense, 6, "default defense is 1")
        self.assertEqual(animal_from_database.speed, 6, "default speed is 1")
        self.assertEqual(animal_from_database.level, 1, "default level is 1")
        self.assertEqual(animal_from_database.experience, 0, "default experience is 0")
    
    def test_remove_animal(self):
        self.animal.save()
        self.animal.delete()
        count = Animal.objects.count()
        self.assertEqual(count, 0, "There should not be any more objects in animals")
