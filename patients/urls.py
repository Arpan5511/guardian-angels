from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.patient_register, name='patient_register'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('profile/', views.patient_profile, name='patient_profile'),
]
