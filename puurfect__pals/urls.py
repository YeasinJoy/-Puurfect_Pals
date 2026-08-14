"""
URL configuration for puurfect__pals project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Adoption import views as s_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', s_views.home, name='home'),
path('about/', s_views.about_page, name='about_page'),
    path('services/', s_views.services_page, name='services_page'),
path('contact/', s_views.contact_page, name='contact_page'),

    path('login/', s_views.login_view, name='login'),
    path('logout/', s_views.logout_view, name='logout'),
    path('register/', s_views.register, name='register'),

    path('search/', s_views.search_pet, name='search_pet'),
    path('doctor/search/', s_views.search_doctor, name='search_doctor'),




    path('pet/', s_views.pet, name='pet'),
# urls.py
path('adopt/<int:id>/', s_views.adopt_pet, name='adopt_pet'),
path('adopt/confirm/<int:id>/', s_views.adopt_confirm, name='adopt_confirm'),



    path('profile/', s_views.profile, name='profile'),
    path('profile/create/', s_views.create_profile, name='create_profile'),
    path('edit_profile/<int:id>/', s_views.edit_profile, name='edit_profile'),

    path('doctor/', s_views.doctor, name='doctor'),
    path('upload_doctor/', s_views.upload_doctor, name='upload_doctor'),
    path('doctor/<int:id>/', s_views.doctor_details, name='doctor_details'),
    path('appointment/<int:doctor_id>/', s_views.make_appointment, name='make_appointment'),
path('appointment/confirm/<int:doctor_id>/', s_views.appointment_confirm, name='appointment_confirm'),




    path('update_doctor/<int:id>/', s_views.update_doctor, name='update_doctor'),
    path('delete_doctor/<int:id>/', s_views.delete_doctor, name='delete_doctor'),

    path('upload_pet/', s_views.upload_pet, name='upload_pet'),
    path('update_pet/<int:id>/', s_views.update_pet, name='update_pet'),
    path('delete_pet/<int:id>/', s_views.delete_pet, name='delete_pet'),
    path('pet/<int:id>/', s_views.pet_details, name='pet_details'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





