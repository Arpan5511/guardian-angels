from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Patient
from .forms import PatientRegistrationForm, PatientProfileForm
from appointments.models import Appointment

def patient_register(request):
    if request.user.is_authenticated:
        return redirect('patient_dashboard')
    
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save()
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
            messages.success(request, "Patient registration successful!")
            return redirect('patient_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'patients/register.html', {'form': form})


@login_required
def patient_dashboard(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, "You are not registered as a patient.")
        return redirect('home')
    
    appointments = patient.appointments.all().order_by('-appointment_date')
    
    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'patients/dashboard.html', context)


@login_required
def patient_profile(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, "You are not registered as a patient.")
        return redirect('home')
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False)
            # Update user info
            patient.user.first_name = form.cleaned_data['first_name']
            patient.user.last_name = form.cleaned_data['last_name']
            patient.user.email = form.cleaned_data['email']
            patient.user.save()
            patient.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('patient_dashboard')
    else:
        form = PatientProfileForm(instance=patient)
    
    return render(request, 'patients/profile.html', {'form': form, 'patient': patient})
