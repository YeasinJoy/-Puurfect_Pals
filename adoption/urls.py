from django.urls import path
from . import views

urlpatterns = [
    path('pets/', views.PetListView.as_view(), name='pet-list'),
    path('pet/<int:pk>/', views.PetDetailView.as_view(), name='pet-detail'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor-list'),
    path('add-pet/', views.add_pet, name='add-pet'),
    path('signup/', views.signup, name='signup'),
]