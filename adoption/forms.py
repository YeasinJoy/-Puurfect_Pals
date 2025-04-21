from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Pet

class SignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'age', 'description', 'image']