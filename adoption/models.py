from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_pet_owner = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)


class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    adopted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    clinic_address = models.TextField()

    def __str__(self):
        return self.name


from django.db import models

# Create your models here.
