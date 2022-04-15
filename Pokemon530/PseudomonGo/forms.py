from django import forms
from .models import AnimalImage

class ImageForm(forms.ModelForm):
    class Meta:
        model = AnimalImage
        fields = ["name", "animal_description", "image_file"]