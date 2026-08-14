from django import forms
from django.forms import ModelForm
from .models import Pet, Doctor, Profile

class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = '__all__'

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class ProfileForm(forms.ModelForm):   # ✅ top-level
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'address', 'profile_picture']