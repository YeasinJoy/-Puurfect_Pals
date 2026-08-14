from django.contrib.auth import authenticate
from django.shortcuts import render,redirect, get_object_or_404
from .models import Profile,Doctor,Pet
from .forms import ProfileForm
from django.contrib.auth import login as auth_login,authenticate,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor, Appointment

# Create your views here.



def home(request):
    # If user is logged in, get pets; else pets = None
    pets = Pet.objects.all() if request.user.is_authenticated else None
    return render(request, 'Adoption/home.html', {'pets': pets})

def about_page(request):
    return render(request, 'Adoption/about.html')

def services_page(request):
    return render(request, 'Adoption/services.html')
def contact_page(request):
    return render(request, 'Adoption/contact.html')

@login_required
@login_required
def profile(request):
    user_profile = Profile.objects.filter(user=request.user).first()

    context = {
        'profile': user_profile,
        'is_admin': request.user.is_staff
    }
    return render(request, 'Adoption/profile.html', context)


def edit_profile(request, id):
    profile = Profile.objects.get(pk=id)

    if request.method == "POST":

        profile.name = request.POST.get("name")
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")


        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        return redirect('profile')

    context = {
        'profile': profile,
    }
    return render(request, 'Adoption/edit_profile.html', context)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # ✅ Admin / superuser → no profile check
            if user.is_staff or user.is_superuser:
                auth_login(request, user)
                return redirect('pet')

            # ✅ Normal user → profile must exist
            if Profile.objects.filter(user=user).exists():
                auth_login(request, user)
                return redirect('pet')
            else:
                messages.error(
                    request,
                    "You must complete your profile first. Please register again."
                )
                return redirect('register')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'Adoption/Login.html')
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        # Password check
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # ✅ Profile mandatory check
        if not (phone or address or profile_picture):
            messages.error(request, "Profile information is mandatory")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        # Create profile
        Profile.objects.create(
            user=user,
            name=user.get_full_name() or user.username,
            phone=phone,
            address=address,
            profile_picture=profile_picture
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'Adoption/register.html')
def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def doctor(request):
    doctors = Doctor.objects.all()
    context = {
        'doctors': doctors,

    }
    return render(request, template_name='Adoption/doctor.html',context=context)


def make_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)



    return render(request, 'Adoption/appointment_success.html', {'doctor': doctor})


@login_required
def upload_doctor(request):
    if not request.user.is_staff:
        messages.error(request, "Only admin can add doctors.")
        return redirect('doctor')

    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor added successfully.")
            return redirect('doctor')
    else:
        form = DoctorForm()

    return render(request, 'Adoption/upload_doctor.html', {'form': form})
@login_required
def update_doctor(request, id):
    if not request.user.is_staff:
        messages.error(request, "Only admin can update doctor information.")
        return redirect('doctor')

    doctor = get_object_or_404(Doctor, pk=id)

    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor updated successfully.")
            return redirect('doctor')
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'Adoption/upload_doctor.html', {'form': form})

@login_required
def delete_doctor(request, id):
    if not request.user.is_staff:
        messages.error(request, "Only admin can delete doctors.")
        return redirect('doctor')

    doctor = get_object_or_404(Doctor, pk=id)

    if request.method == "POST":
        doctor.delete()
        messages.success(request, "Doctor deleted successfully.")
        return redirect('doctor')

    return render(request, 'Adoption/delete_doctor.html', {'doctor': doctor})

from django.shortcuts import render
from .models import Pet
@login_required
def pet(request):
    # Get all pets ordered by newest first
    pets = Pet.objects.all().order_by('-id')  # newest pets first

    # Count for summary box
    total_count = pets.count()
    available_count = pets.filter(status='available').count()
    adopted_count = pets.filter(status='adopted').count()
    pending_count = pets.filter(status='pending').count()

    # Filter if clicked on summary box
    filter_status = request.GET.get('status')
    if filter_status in ['available', 'adopted', 'pending']:
        pets = pets.filter(status=filter_status)

    context = {
        'pets': pets,
        'total_count': total_count,
        'available_count': available_count,
        'adopted_count': adopted_count,
        'pending_count': pending_count,

    }
    return render(request, 'Adoption/pet.html', context)


@login_required
def pet_details(request,id):
    pet = Pet.objects.get(pk=id)

    context = {
        'pet': pet,
        'is_admin': request.user.is_staff
    }
    return render(request, template_name='Adoption/pet_details.html',context=context)


def upload_pet(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pet')
    else:
        form = PetForm()

    context = {
        'form': form,
    }
    return render(request, 'Adoption/upload_pet.html', context)


from django.shortcuts import get_object_or_404

@login_required
def update_pet(request, id):
    if not request.user.is_staff:
        messages.error(request, "Only admin can update pet information.")
        return redirect('pet')

    pet = get_object_or_404(Pet, pk=id)

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet updated successfully.")
            return redirect('pet')
    else:
        form = PetForm(instance=pet)

    return render(request, 'Adoption/upload_pet.html', {'form': form})

@login_required
def delete_pet(request, id):
    if not request.user.is_staff:
        messages.error(request, "Only admin can delete pets.")
        return redirect('pet')

    pet = get_object_or_404(Pet, pk=id)

    if request.method == "POST":
        pet.delete()
        messages.success(request, "Pet deleted successfully.")
        return redirect('pet')

    return render(request, 'Adoption/delete_pet.html', {'pet': pet})

def search_pet(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return redirect('pet')

    pets = Pet.objects.filter(Q(name__icontains=query))

    if pets.count() == 1:
        return redirect('pet_details', id=pets.first().id)
    else:
        # Pass the pets (even 0 or many) to the pet.html page
        if not pets.exists():
            messages.warning(request, f'No pets found matching "{query}".')
        return render(request, 'Adoption/pet.html', {'pets': pets})


def search_doctor(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return redirect('doctor')

    doctors = Doctor.objects.filter(Q(name__icontains=query))

    if doctors.count() == 1:
        return redirect('doctor_details', id=doctors.first().id)
    elif doctors.exists():
        return render(request, 'Adoption/search_doctor_result.html', {
            'doctors': doctors,
            'query': query
        })
    else:
        messages.warning(request, f'No doctors found matching "{query}".')
        return redirect('doctor')


@login_required
def adopt_pet(request, id):
    # 🚫 Admin cannot adopt
    if request.user.is_staff:
        messages.error(request, "Admin cannot adopt pets.")
        return redirect('pet')
    pet = get_object_or_404(Pet, id=id)

    if pet.status == 'available':
        pet.status = 'adopted'
        pet.save()

    return redirect('pet')

@login_required
def adopt_confirm(request, id):
    pet = get_object_or_404(Pet, id=id)

    if request.method == 'POST':
        # Yes চাপলে
        if pet.status == 'available':
            pet.status = 'adopted'
            pet.save()
        return redirect('pet')

    # GET request → confirmation page দেখাবে
    return render(request, 'Adoption/adopt_confirm.html', {'pet': pet})



@login_required
def doctor_details(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    today = timezone.now().date()

    # check if current user already has an appointment today with this doctor
    existing_appointment = Appointment.objects.filter(
        user=request.user,
        doctor=doctor,
        date=today
    ).first()

    # total appointments for this doctor
    total_appointments = Appointment.objects.filter(doctor=doctor, date=today).count()

    context = {
        'doctor': doctor,
        'existing_appointment': existing_appointment,
        'total_appointments': total_appointments,
    }
    return render(request, 'Adoption/doctor_details.html', context)

@login_required
def appointment_confirm(request, doctor_id):

    doctor = get_object_or_404(Doctor, id=doctor_id)
    today = timezone.now().date()

    # Check if user already booked
    existing_appointment = Appointment.objects.filter(
        doctor=doctor,
        user=request.user,
        date=today
    ).first()

    if existing_appointment:
        return render(request, 'Adoption/appointment_confirm.html', {
            'doctor': doctor,
            'serial': existing_appointment.serial_number,
            'date': today,
            'already_booked': True
        })

    # Find next serial number
    last_appointment = Appointment.objects.filter(doctor=doctor, date=today).order_by('-serial_number').first()
    next_serial = 1 if not last_appointment else last_appointment.serial_number + 1

    if request.method == 'POST':
        # create appointment
        appointment = Appointment.objects.create(
            user=request.user,
            doctor=doctor,
            date=today,
            serial_number=next_serial
        )
        return render(request, 'Adoption/appointment_confirm.html', {
            'doctor': doctor,
            'serial': appointment.serial_number,
            'date': today,
            'already_booked': True
        })

    return render(request, 'Adoption/appointment_confirm.html', {
        'doctor': doctor,
        'serial': next_serial,
        'date': today,
        'already_booked': False
    })


@login_required
def create_profile(request):
    # Superuser check
    is_admin = request.user.is_superuser
    # Check if profile already exists for this user
    if Profile.objects.filter(user=request.user).exists():
        return redirect('profile')  # redirect if already exists

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm()
        context = {
            'form': form,
            'show_name': "Admin" if is_admin else None
        }

    return render(request, 'Adoption/create_profile.html', {'form': form})


