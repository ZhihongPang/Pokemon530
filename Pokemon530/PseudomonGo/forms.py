from django import forms
from .models import Animal

class ImageForm(forms.ModelForm):
    class Meta:
        model = Animal
        # fields = ["player", "animal_name", "animal_description", 
        #           "photo_path", "animal_species", "animal_class"]
        fields = ["animal_name", "animal_description", "photo_path"]