from django import forms
from .models import Appointment

class AppointmentBookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'symptoms']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'symptoms': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your symptoms...'}),
        }


class AppointmentCancellationForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['cancellation_reason']
        widgets = {
            'cancellation_reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Reason for cancellation...'}),
        }
