from django import forms
from django.contrib.auth.models import User
from .models import Doctor, DoctorTiming

class DoctorRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")
    
    class Meta:
        model = Doctor
        fields = ['specialization', 'license_number', 'experience_years', 'phone', 'bio', 'consultation_fee']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        email = cleaned_data.get('email')
        
        # Check if email already exists
        if email and User.objects.filter(username=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different email or login.")
        
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        doctor = super().save(commit=False)
        doctor.user = user
        if commit:
            doctor.save()
        return doctor


class DoctorTimingForm(forms.ModelForm):
    class Meta:
        model = DoctorTiming
        fields = ['day', 'start_time', 'end_time', 'slot_duration', 'is_available']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class DoctorProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Doctor
        fields = ['specialization', 'experience_years', 'phone', 'bio', 'consultation_fee', 'is_available']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
