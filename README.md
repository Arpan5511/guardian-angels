# Guardian Angels - Doctor Appointment Booking System

A comprehensive web application for booking doctor appointments with features for both doctors and patients.

## Features

### For Patients
- User registration and login
- Browse and search doctors by specialization
- View doctor profiles and availability
- Book appointments with time slot selection
- View appointment history and details
- Cancel appointments with reason
- Manage medical history and allergies
- Update profile information

### For Doctors
- User registration and login
- Set working hours and availability for each day
- Manage appointment slots with configurable slot duration
- View all appointments
- Confirm pending appointments
- Mark appointments as completed
- Update profile and specialization details
- Track consultation fees

### General Features
- Beautiful Bootstrap-based responsive UI
- Secure authentication and authorization
- Real-time slot availability checking
- Appointment status tracking (Pending, Confirmed, Completed, Cancelled)
- MySQL database integration with XAMPP
- Admin panel for managing users and appointments

## Technology Stack

- **Backend**: Python Django 4.2
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: MySQL (via XAMPP)
- **Server**: Django Development Server

## Prerequisites

- Python 3.8+
- XAMPP with MySQL
- pip (Python package manager)

## Installation & Setup

### 1. Install XAMPP

Download and install XAMPP from: https://www.apachefriends.org/
- Start MySQL service from XAMPP Control Panel

### 2. Create MySQL Database

Open phpMyAdmin (usually at http://localhost/phpmyadmin)

```sql
CREATE DATABASE guardian_angels;
```

### 3. Clone/Extract Project

Extract the project to your desired location.

### 4. Install Python Dependencies

Navigate to project directory and run:

```bash
pip install -r requirements.txt
```

If you face issues with mysqlclient:
- On Windows: `pip install mysqlclient` (may require Visual C++ Build Tools)
- Alternative: Use `PyMySQL` instead of `mysqlclient`

To use PyMySQL, add this to `guardian_angels/settings.py` right after imports:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

And update `requirements.txt`:
```
Django==4.2.0
PyMySQL==1.1.0
```

### 5. Configure Database Connection

Update database settings in `guardian_angels/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'guardian_angels',
        'USER': 'root',  # XAMPP default username
        'PASSWORD': '',  # XAMPP default password (empty)
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow prompts to create admin account.

### 8. Start Development Server

```bash
python manage.py runserver
```

The application will be available at: http://localhost:8000

## Usage

### Admin Panel
- URL: http://localhost:8000/admin
- Use superuser credentials created during setup

### Patient Registration
1. Go to Home page → Click "Register as Patient"
2. Fill in personal and medical details
3. Set password and confirm
4. Submit to register

### Doctor Registration
1. Go to Home page → Click "Register as Doctor"
2. Fill in professional details (specialization, license, etc.)
3. Set consultation fee
4. Submit to register
5. Log in to dashboard
6. Go to "Add Timing" to set working hours for each day

### Booking Appointment (Patient)
1. Log in as patient
2. Go to "Find Doctors"
3. Search by specialization (optional)
4. Click on doctor to view profile
5. Click "Book Appointment"
6. Select date
7. Choose available time slot
8. Describe symptoms
9. Confirm booking

### Managing Appointments (Doctor)
1. Log in as doctor
2. View all appointments in dashboard
3. Confirm pending appointments
4. Mark confirmed appointments as completed
5. View appointment details and patient symptoms

### Cancel Appointment (Patient)
1. Log in as patient
2. Go to "Patient Dashboard"
3. Find appointment you want to cancel
4. Click "Cancel" button
5. Provide cancellation reason
6. Confirm cancellation

## Project Structure

```
guardian_angels/
├── guardian_angels/          # Project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # URL routing
│   ├── auth_views.py        # Authentication views
│   └── wsgi.py              # WSGI application
├── doctors/                 # Doctor app
│   ├── models.py            # Doctor and DoctorTiming models
│   ├── views.py             # Doctor views
│   ├── forms.py             # Doctor forms
│   ├── urls.py              # Doctor URLs
│   └── admin.py             # Admin configuration
├── patients/                # Patient app
│   ├── models.py            # Patient model
│   ├── views.py             # Patient views
│   ├── forms.py             # Patient forms
│   ├── urls.py              # Patient URLs
│   └── admin.py             # Admin configuration
├── appointments/            # Appointment app
│   ├── models.py            # Appointment model
│   ├── views.py             # Appointment views
│   ├── forms.py             # Appointment forms
│   ├── urls.py              # Appointment URLs
│   └── admin.py             # Admin configuration
├── templates/               # HTML templates
│   ├── base.html            # Base template with navbar
│   ├── index.html           # Home page
│   ├── login.html           # Login page
│   ├── doctors/             # Doctor templates
│   ├── patients/            # Patient templates
│   └── appointments/        # Appointment templates
├── static/                  # Static files
│   ├── css/                 # CSS files
│   └── js/                  # JavaScript files
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## Database Models

### Doctor
- User (OneToOne)
- Specialization
- License Number
- Experience Years
- Phone
- Bio
- Consultation Fee
- Is Available

### DoctorTiming
- Doctor (ForeignKey)
- Day (Monday-Sunday)
- Start Time
- End Time
- Slot Duration
- Is Available

### Patient
- User (OneToOne)
- Date of Birth
- Gender
- Phone
- Address
- City, State, Pincode
- Medical History
- Allergies

### Appointment
- Doctor (ForeignKey)
- Patient (ForeignKey)
- Appointment Date & Time
- Status (Pending, Confirmed, Completed, Cancelled)
- Symptoms
- Cancellation Reason
- Timestamps

## API Endpoints

### Appointment Slots
GET `/appointments/available-slots/<doctor_id>/?date=YYYY-MM-DD`

Returns available time slots for a doctor on a given date.

## Troubleshooting

### MySQL Connection Error
- Ensure XAMPP MySQL is running
- Check database name and credentials in settings.py
- Verify database exists: `SHOW DATABASES;`

### Module Import Errors
- Ensure all apps are installed in INSTALLED_APPS
- Run migrations: `python manage.py migrate`

### Template Not Found
- Check template path is in TEMPLATES directories
- Clear browser cache and restart server

### Time Slot Not Showing
- Ensure doctor has set working hours for the date
- Check day name matches (Monday-Sunday lowercase)

## Security Notes

1. Change SECRET_KEY in production: `settings.py`
2. Set DEBUG = False in production
3. Use strong passwords
4. Enable HTTPS in production
5. Use environment variables for sensitive data

## Future Enhancements

- Payment gateway integration
- Email notifications
- SMS notifications
- Video consultation
- Prescription management
- Medicine ordering
- Rating and reviews system
- Insurance integration

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please contact: info@guardianangels.com

---

**Built with ❤️ for better healthcare access**
