import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import AnimalImage
from PseudomonGo.models import EntityClass
import base64


### Tests for Animal Upload ###
class AnimalModelTests(TestCase):
    # if you failed any of these then check AnimalImage in models to see if database fields have been initialized correctly
    def test_animal_pub_time(self):
        animal = AnimalImage()
        self.assertIs(animal.was_published_recently(), True)
    def test_animal_name(self):
        animal = AnimalImage()
        animal.name = "Horse"
        self.assertIs(animal.has_animal_name(), "Horse")
    def test_animal_description(self):
        animal=AnimalImage()
        animal.animal_description = "This is a horse, trust me bro"
        self.assertIs(animal.has_animal_description(), "This is a horse, trust me bro")
    # if you failed this test, then there might be ghost images attached to newly initialized animals
    def test_animal_image(self):
        animal = AnimalImage()
        self.assertNotEqual(animal.image_file, True)
    
    # tests to see if the animal upload is correctly reflected in the database
    def test_animal_upload_name(self):
        animal = AnimalImage()
        animal.name = "Horse"
        animal.save()
        animal_from_database = AnimalImage.objects.last() # the last entry to the databse should be made by the test case
        self.assertEqual(animal_from_database.name, animal.name)
    def test_animal_upload_description(self):
        animal = AnimalImage()
        animal.animal_description = "This is a horse, trust me bro"
        animal.save()
        animal_from_database = AnimalImage.objects.last()
        self.assertEqual(animal_from_database.animal_description, animal.animal_description)
    def test_animal_upload_image_file(self):
        animal = AnimalImage()
        animal.image_file = "images/download.jpg"
        animal.save()
        animal_from_database = AnimalImage.objects.last()
        self.assertEqual(animal_from_database.image_file, animal.image_file)
        

# Create your tests here.
class EntityClassTestCase(TestCase):
    def setUp(self):
        EntityClass.objects.create(class_name="Foo", class_description="Bar")
        EntityClass.objects.create(class_name="Baz", class_description="ABC")

    def test_entities_class(self):
        """classes are assigned names properly"""
        en_1 = EntityClass.objects.get(class_name="Foo")
        en_2 = EntityClass.objects.get(class_name="Baz")
        self.assertEqual(str(en_1), 'Foo')
        self.assertEqual(str(en_1), 'Baz')
