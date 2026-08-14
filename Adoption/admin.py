from django.contrib import admin
from .models import Profile,Doctor, Pet
# Register your models here.
admin.site.register([Profile,Doctor,Pet])