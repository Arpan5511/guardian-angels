"""
Management command to populate initial data for demo
Run with: python manage.py populate_demo_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from doctors.models import Doctor, DoctorTiming
from patients.models import Patient
from datetime import date

class Command(BaseCommand):
    help = 'Populate demo data for testing'

    def handle(self, *args, **options):
        # Create demo doctors
        doctor_data = [
            {
                'first_name': 'Rajesh',
                'last_name': 'Sharma',
                'email': 'dr.rajesh@guardianangels.com',
                'password': 'password123',
                'specialization': 'cardiology',
                'license': 'LIC001',
                'experience': 15,
                'phone': '9876543210',
                'fee': 500,
                'bio': 'Senior Cardiologist with 15 years of experience in treating heart diseases.'
            },
            {
                'first_name': 'Priya',
                'last_name': 'Patel',
                'email': 'dr.priya@guardianangels.com',
                'password': 'password123',
                'specialization': 'dermatology',
                'license': 'LIC002',
                'experience': 10,
                'phone': '9876543211',
                'fee': 400,
                'bio': 'Expert dermatologist specializing in skin disorders and cosmetic treatments.'
            },
            {
                'first_name': 'Amit',
                'last_name': 'Singh',
                'email': 'dr.amit@guardianangels.com',
                'password': 'password123',
                'specialization': 'orthopedics',
                'license': 'LIC003',
                'experience': 12,
                'phone': '9876543212',
                'fee': 450,
                'bio': 'Orthopedic surgeon with expertise in joint replacement and sports medicine.'
            },
            {
                'first_name': 'Neha',
                'last_name': 'Gupta',
                'email': 'dr.neha@guardianangels.com',
                'password': 'password123',
                'specialization': 'pediatrics',
                'license': 'LIC004',
                'experience': 8,
                'phone': '9876543213',
                'fee': 300,
                'bio': 'Pediatrician caring for children with focus on preventive health.'
            },
        ]

        for doc in doctor_data:
            user = User.objects.create_user(
                username=doc['email'],
                email=doc['email'],
                password=doc['password'],
                first_name=doc['first_name'],
                last_name=doc['last_name']
            )
            doctor = Doctor.objects.create(
                user=user,
                specialization=doc['specialization'],
                license_number=doc['license'],
                experience_years=doc['experience'],
                phone=doc['phone'],
                consultation_fee=doc['fee'],
                bio=doc['bio'],
                is_available=True
            )
            
            # Create sample timings
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            for day in days:
                DoctorTiming.objects.create(
                    doctor=doctor,
                    day=day,
                    start_time='09:00',
                    end_time='17:00',
                    slot_duration=30,
                    is_available=True
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully created demo doctors'))

        # Create demo patients
        patient_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'password': 'password123',
                'dob': '1990-01-15',
                'gender': 'male',
                'phone': '9123456789',
                'address': '123 Main St',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400001',
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Smith',
                'email': 'sarah.smith@example.com',
                'password': 'password123',
                'dob': '1988-05-20',
                'gender': 'female',
                'phone': '9123456790',
                'address': '456 Park Ave',
                'city': 'Delhi',
                'state': 'Delhi',
                'pincode': '110001',
            },
        ]

        for pat in patient_data:
            user = User.objects.create_user(
                username=pat['email'],
                email=pat['email'],
                password=pat['password'],
                first_name=pat['first_name'],
                last_name=pat['last_name']
            )
            Patient.objects.create(
                user=user,
                date_of_birth=pat['dob'],
                gender=pat['gender'],
                phone=pat['phone'],
                address=pat['address'],
                city=pat['city'],
                state=pat['state'],
                pincode=pat['pincode'],
            )

        self.stdout.write(self.style.SUCCESS('Successfully created demo patients'))
