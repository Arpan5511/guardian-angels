from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.doctor_register, name='doctor_register'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('profile/', views.doctor_profile, name='doctor_profile'),
    path('add-timing/', views.add_timing, name='add_timing'),
    path('edit-timing/<int:timing_id>/', views.edit_timing, name='edit_timing'),
    path('delete-timing/<int:timing_id>/', views.delete_timing, name='delete_timing'),
    path('list/', views.doctor_list, name='doctor_list'),
    path('detail/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
]
