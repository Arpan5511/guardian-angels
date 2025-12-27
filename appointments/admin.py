from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at']
    search_fields = ['patient__user__first_name', 'doctor__user__first_name', 'status']
    list_filter = ['status', 'appointment_date', 'created_at']
    date_hierarchy = 'appointment_date'
