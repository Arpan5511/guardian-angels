from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from doctors.models import Doctor, DoctorTiming
from patients.models import Patient
from .models import Appointment
from .forms import AppointmentBookingForm, AppointmentCancellationForm

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, "Please register as a patient first.")
        return redirect('patient_register')
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = patient
            
            # Check if slot is already booked
            existing_appointment = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment.appointment_date,
                appointment_time=appointment.appointment_time,
                status__in=['pending', 'confirmed']
            ).exists()
            
            if existing_appointment:
                messages.error(request, "This time slot is already booked. Please select another time.")
                return render(request, 'appointments/book_appointment.html', {
                    'form': form,
                    'doctor': doctor,
                })
            
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, "Appointment booked successfully! Please wait for confirmation.")
            return redirect('patient_dashboard')
    else:
        form = AppointmentBookingForm()
    
    context = {
        'form': form,
        'doctor': doctor,
    }
    return render(request, 'appointments/book_appointment.html', context)


@login_required
def get_available_slots(request, doctor_id):
    """API endpoint to get available time slots for a doctor on a given date"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    date_str = request.GET.get('date')
    
    if not date_str:
        return JsonResponse({'error': 'Date parameter required'}, status=400)
    
    try:
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    # Get the day of week (0=Monday, 6=Sunday)
    day_name = appointment_date.strftime('%A').lower()
    
    # Get doctor's timing for this day
    timing = doctor.timings.filter(day=day_name, is_available=True).first()
    
    if not timing:
        return JsonResponse({'slots': []})
    
    # Generate available slots
    slots = []
    current_time = datetime.combine(appointment_date, timing.start_time)
    end_time = datetime.combine(appointment_date, timing.end_time)
    slot_duration = timedelta(minutes=timing.slot_duration)
    
    booked_slots = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date,
        status__in=['pending', 'confirmed']
    ).values_list('appointment_time', flat=True)
    
    booked_times = [str(slot) for slot in booked_slots]
    
    while current_time < end_time:
        slot_time = current_time.time()
        slot_time_str = str(slot_time)
        
        if slot_time_str not in booked_times:
            slots.append({
                'time': slot_time_str,
                'display': current_time.strftime('%I:%M %p')
            })
        
        current_time += slot_duration
    
    return JsonResponse({'slots': slots})


@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user is the patient or doctor
    try:
        patient = Patient.objects.get(user=request.user)
        if appointment.patient != patient:
            messages.error(request, "Unauthorized access!")
            return redirect('patient_dashboard')
    except Patient.DoesNotExist:
        try:
            doctor = Doctor.objects.get(user=request.user)
            if appointment.doctor != doctor:
                messages.error(request, "Unauthorized access!")
                return redirect('doctor_dashboard')
        except Doctor.DoesNotExist:
            messages.error(request, "Unauthorized access!")
            return redirect('home')
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'appointments/appointment_detail.html', context)


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user is the patient
    try:
        patient = Patient.objects.get(user=request.user)
        if appointment.patient != patient:
            messages.error(request, "Unauthorized access!")
            return redirect('patient_dashboard')
    except Patient.DoesNotExist:
        messages.error(request, "You are not registered as a patient.")
        return redirect('patient_register')
    
    # Check if appointment can be cancelled
    if appointment.status == 'cancelled':
        messages.error(request, "This appointment is already cancelled.")
        return redirect('patient_dashboard')
    
    if appointment.status == 'completed':
        messages.error(request, "Cannot cancel a completed appointment.")
        return redirect('patient_dashboard')
    
    if request.method == 'POST':
        form = AppointmentCancellationForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment.status = 'cancelled'
            appointment.cancelled_at = datetime.now()
            appointment.save()
            messages.success(request, "Appointment cancelled successfully!")
            return redirect('patient_dashboard')
    else:
        form = AppointmentCancellationForm(instance=appointment)
    
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'appointments/cancel_appointment.html', context)


@login_required
def confirm_appointment(request, appointment_id):
    """Doctor confirms an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user is the doctor
    try:
        doctor = Doctor.objects.get(user=request.user)
        if appointment.doctor != doctor:
            messages.error(request, "Unauthorized access!")
            return redirect('doctor_dashboard')
    except Doctor.DoesNotExist:
        messages.error(request, "You are not registered as a doctor.")
        return redirect('doctor_register')
    
    if request.method == 'POST':
        if appointment.status == 'pending':
            appointment.status = 'confirmed'
            appointment.save()
            messages.success(request, "Appointment confirmed!")
        else:
            messages.error(request, "Cannot confirm this appointment.")
        return redirect('doctor_dashboard')
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'appointments/confirm_appointment.html', context)


@login_required
def complete_appointment(request, appointment_id):
    """Doctor marks an appointment as completed"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user is the doctor
    try:
        doctor = Doctor.objects.get(user=request.user)
        if appointment.doctor != doctor:
            messages.error(request, "Unauthorized access!")
            return redirect('doctor_dashboard')
    except Doctor.DoesNotExist:
        messages.error(request, "You are not registered as a doctor.")
        return redirect('doctor_register')
    
    if request.method == 'POST':
        if appointment.status == 'confirmed':
            appointment.status = 'completed'
            appointment.save()
            messages.success(request, "Appointment marked as completed!")
        else:
            messages.error(request, "Only confirmed appointments can be completed.")
        return redirect('doctor_dashboard')
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'appointments/complete_appointment.html', context)
