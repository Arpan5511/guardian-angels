from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone', 'city', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'email', 'phone']
    list_filter = ['city', 'created_at']
