from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Pet, Doctor
from .forms import SignUpForm, PetForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('pet-list')
    else:
        form = PetForm()
    return render(request, 'adoption/add_pet.html', {'form': form})

class PetListView(ListView):
    model = Pet
    template_name = 'adoption/pet_list.html'

class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'adoption/pet_detail.html'

class DoctorListView(ListView):
    model = Doctor
    template_name = 'adoption/doctor_list.html'