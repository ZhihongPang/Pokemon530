import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from PseudomonGo.models import EntityClass

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
        self.assertEqual(str(en_2), 'Baz')
