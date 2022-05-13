from django import forms
from .models import Animal, User
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.core.exceptions import ValidationError
import unicodedata
from django.utils.translation import gettext_lazy as _

# forms for upload/removal of animals
class UploadForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ["animal_name", "animal_description", "animal_location",
                  "photo_path", "animal_species", "animal_class"]

class RateAnimalForm(forms.Form):
    rating = forms.TypedChoiceField(
        choices=(("5", "⭐⭐⭐⭐⭐"), ("4", "⭐⭐⭐⭐"), ("3", "⭐⭐⭐"), ("2", "⭐⭐"), ("1", "⭐")),
        coerce=int,
        required=True,
    )
'''
Forms for signing up new users
'''
class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize("NFKC", super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "username",
        }

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("email", "username",)
        field_classes = {
            "email": forms.EmailField,
            "username": UsernameField
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.EMAIL_FIELD in self.fields:
            self.fields[self._meta.model.EMAIL_FIELD].widget.attrs[
                "autofocus"
            ] = True
        self.fields['email'].required = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user