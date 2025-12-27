from django.contrib import admin
from .models import Doctor, DoctorTiming

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'specialization', 'license_number', 'is_available', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    list_filter = ['specialization', 'is_available', 'created_at']

@admin.register(DoctorTiming)
class DoctorTimingAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day', 'start_time', 'end_time', 'slot_duration', 'is_available']
    list_filter = ['day', 'is_available']
