from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Doctor, DoctorTiming
from .forms import DoctorRegistrationForm, DoctorTimingForm, DoctorProfileForm
from appointments.models import Appointment

@login_required
def doctor_dashboard(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, "You are not registered as a doctor.")
        return redirect('home')
    
    appointments = doctor.appointments.all().order_by('-appointment_date')
    timings = doctor.timings.all()
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'timings': timings,
    }
    return render(request, 'doctors/dashboard.html', context)


def doctor_register(request):
    if request.user.is_authenticated:
        return redirect('doctor_dashboard')
    
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
            messages.success(request, "Doctor registration successful!")
            return redirect('doctor_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'doctors/register.html', {'form': form})


@login_required
def doctor_profile(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, "You are not registered as a doctor.")
        return redirect('home')
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor = form.save(commit=False)
            # Update user info
            doctor.user.first_name = form.cleaned_data['first_name']
            doctor.user.last_name = form.cleaned_data['last_name']
            doctor.user.email = form.cleaned_data['email']
            doctor.user.save()
            doctor.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('doctor_dashboard')
    else:
        form = DoctorProfileForm(instance=doctor)
    
    return render(request, 'doctors/profile.html', {'form': form, 'doctor': doctor})


@login_required
def add_timing(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, "You are not registered as a doctor.")
        return redirect('home')
    
    if request.method == 'POST':
        form = DoctorTimingForm(request.POST)
        if form.is_valid():
            timing = form.save(commit=False)
            timing.doctor = doctor
            timing.save()
            messages.success(request, "Timing added successfully!")
            return redirect('doctor_dashboard')
    else:
        form = DoctorTimingForm()
    
    return render(request, 'doctors/add_timing.html', {'form': form})


@login_required
def edit_timing(request, timing_id):
    timing = get_object_or_404(DoctorTiming, id=timing_id)
    
    if timing.doctor.user != request.user:
        messages.error(request, "Unauthorized access!")
        return redirect('doctor_dashboard')
    
    if request.method == 'POST':
        form = DoctorTimingForm(request.POST, instance=timing)
        if form.is_valid():
            form.save()
            messages.success(request, "Timing updated successfully!")
            return redirect('doctor_dashboard')
    else:
        form = DoctorTimingForm(instance=timing)
    
    return render(request, 'doctors/edit_timing.html', {'form': form, 'timing': timing})


@login_required
def delete_timing(request, timing_id):
    timing = get_object_or_404(DoctorTiming, id=timing_id)
    
    if timing.doctor.user != request.user:
        messages.error(request, "Unauthorized access!")
        return redirect('doctor_dashboard')
    
    if request.method == 'POST':
        timing.delete()
        messages.success(request, "Timing deleted successfully!")
        return redirect('doctor_dashboard')
    
    return render(request, 'doctors/delete_timing.html', {'timing': timing})


def doctor_list(request):
    specialization = request.GET.get('specialization', '')
    doctors = Doctor.objects.filter(is_available=True)
    
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    context = {
        'doctors': doctors,
        'selected_specialization': specialization,
    }
    return render(request, 'doctors/doctor_list.html', context)


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    timings = doctor.timings.filter(is_available=True)
    
    context = {
        'doctor': doctor,
        'timings': timings,
    }
    return render(request, 'doctors/doctor_detail.html', context)
