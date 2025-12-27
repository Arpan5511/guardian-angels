from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('dermatology', 'Dermatology'),
        ('psychology', 'Psychology'),
        ('general', 'General Practice'),
        ('gynecology', 'Gynecology'),
        ('urology', 'Urology'),
        ('oncology', 'Oncology'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=100, unique=True)
    experience_years = models.IntegerField()
    phone = models.CharField(max_length=15)
    bio = models.TextField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class DoctorTiming(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='timings')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration = models.IntegerField(default=30, help_text="Duration in minutes")
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['doctor', 'day']
        ordering = ['day', 'start_time']
    
    def __str__(self):
        return f"{self.doctor} - {self.day} ({self.start_time} - {self.end_time})"
