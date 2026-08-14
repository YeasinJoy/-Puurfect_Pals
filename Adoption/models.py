from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=20,null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100, default="Dr. Unknown")
    specialization = models.CharField(max_length=100)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)
    contact = models.CharField(max_length=100)
    clinic_address = models.TextField()

    def __str__(self):
        return self.name



class Pet(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('adopted', 'Adopted'),
        ('pending', 'Pending Approval'),
    ]

    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()

    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'  # 👈 important
    )

    def __str__(self):
        return self.name
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    serial_number = models.IntegerField()

    def __str__(self):
        return f"{self.doctor.name} - {self.date} - Serial {self.serial_number}"