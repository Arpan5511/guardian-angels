# Guardian Angels - Setup & Installation Guide

## Quick Start (Windows)

### Step 1: Install XAMPP
1. Download XAMPP from: https://www.apachefriends.org/
2. Run the installer and select MySQL and Apache
3. Complete the installation

### Step 2: Start MySQL
1. Open XAMPP Control Panel
2. Click "Start" button for MySQL module
3. MySQL should be running on port 3306

### Step 3: Create Database
1. Open any browser and go to: http://localhost/phpmyadmin
2. Click "New" on the left panel
3. Create database named: `guardian_angels`
4. Click "Create"

### Step 4: Install Python Dependencies
Open Command Prompt and navigate to the project folder:

```bash
cd "path\to\guardian_angels"
```

Install required packages:
```bash
pip install -r requirements.txt
```

If you have trouble with mysqlclient:
```bash
pip install mysqlclient
```

OR use PyMySQL instead:
```bash
pip install PyMySQL
```

Then add this at the top of `guardian_angels/settings.py` (after imports):
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Step 5: Run Database Migrations
```bash
python manage.py migrate
```

This will create all necessary database tables.

### Step 6: Create Admin Account
```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username: admin
- Email: admin@guardianangels.com
- Password: (enter your password)

### Step 7: Populate Demo Data (Optional)
To add sample doctors and patients for testing:

```bash
python manage.py populate_demo_data
```

### Step 8: Start the Server
```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 9: Access the Application
Open your browser and go to:
- **Main Site**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## Demo Credentials (if you ran populate_demo_data)

### Doctor Accounts:
- Email: dr.rajesh@guardianangels.com
- Password: password123

- Email: dr.priya@guardianangels.com
- Password: password123

### Patient Accounts:
- Email: john.doe@example.com
- Password: password123

- Email: sarah.smith@example.com
- Password: password123

### Admin Account:
- Username: admin (or what you set)
- Password: (what you set)

## Project Structure Overview

```
guardian_angels/
├── guardian_angels/           # Main project folder
│   ├── settings.py           # Database and app configuration
│   ├── urls.py               # Main URL routing
│   └── auth_views.py         # Login/logout views
├── doctors/                  # Doctor management app
│   ├── models.py             # Doctor database models
│   ├── views.py              # Doctor view logic
│   ├── forms.py              # Doctor forms
│   └── urls.py               # Doctor URLs
├── patients/                 # Patient management app
│   ├── models.py             # Patient database models
│   ├── views.py              # Patient view logic
│   ├── forms.py              # Patient forms
│   └── urls.py               # Patient URLs
├── appointments/             # Appointment management app
│   ├── models.py             # Appointment database models
│   ├── views.py              # Appointment view logic
│   ├── forms.py              # Appointment forms
│   └── urls.py               # Appointment URLs
├── templates/                # HTML templates (with Bootstrap)
│   ├── base.html            # Base template with navbar
│   ├── index.html           # Home page
│   ├── login.html           # Login page
│   ├── doctors/             # Doctor templates
│   ├── patients/            # Patient templates
│   └── appointments/        # Appointment templates
├── static/                   # CSS, JS, images
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation

```

## Key Features Walkthrough

### 1. Patient Registration
- Go to Home → "Register as Patient"
- Fill in personal and medical information
- Create account with email and password
- After registration, automatically logged in

### 2. Doctor Registration
- Go to Home → "Register as Doctor"
- Fill in professional details
- Set consultation fees
- After registration, log in to dashboard

### 3. Setting Doctor Timings
- Doctor logs in → Dashboard
- Click "Add Timing"
- Select day of week (Monday-Sunday)
- Set start time, end time, slot duration
- Mark as available
- Repeat for each working day

### 4. Booking Appointment
- Patient logs in → "Find Doctors"
- Search by specialization (optional)
- Click on doctor to view profile
- Click "Book Appointment"
- Select date → Time slot appears
- Select time slot
- Describe symptoms
- Click "Confirm Booking"

### 5. Managing Appointments
Doctor Dashboard:
- View all appointments
- Confirm pending appointments
- Mark confirmed as completed

Patient Dashboard:
- View booked appointments
- Cancel appointment (with reason)
- View appointment details

## Database Structure

### Doctor Table
- ID, User, Specialization, License, Experience, Phone, Fee, Bio, Available, Timestamps

### DoctorTiming Table
- ID, Doctor, Day, Start Time, End Time, Slot Duration, Available

### Patient Table
- ID, User, DOB, Gender, Phone, Address, City, State, Pincode, Medical History, Allergies, Timestamps

### Appointment Table
- ID, Doctor, Patient, Date, Time, Status, Symptoms, Notes, Cancelled Reason, Timestamps

## Troubleshooting

### Issue: "No module named 'mysql'"
**Solution:**
```bash
pip install PyMySQL
```

Then add to `guardian_angels/settings.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Issue: "Access denied for user 'root'"
**Solution:**
- Ensure MySQL is running in XAMPP
- Verify credentials in settings.py match your MySQL setup
- Default: User='root', Password='' (empty)

### Issue: "relation 'doctors_doctor' does not exist"
**Solution:**
```bash
python manage.py migrate
```

### Issue: "TemplateDoesNotExist"
**Solution:**
- Ensure template files exist in templates/ folder
- Check TEMPLATES setting in settings.py
- Restart Django server

### Issue: "Static files not loading"
**Solution:**
```bash
python manage.py collectstatic
```

## Common Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Create superuser non-interactively
python manage.py createsuperuser --username admin --email admin@test.com

# Populate demo data
python manage.py populate_demo_data

# Access Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic --noinput
```

## SQL Commands for MySQL

```sql
-- Check if database exists
SHOW DATABASES;

-- Select database
USE guardian_angels;

-- View all tables
SHOW TABLES;

-- View table structure
DESCRIBE doctors_doctor;

-- Count records
SELECT COUNT(*) FROM doctors_doctor;
```

## Configuration Tips

### Increase Maximum Upload Size
In `settings.py`:
```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
```

### Set Timezone
In `settings.py`:
```python
TIME_ZONE = 'Asia/Kolkata'  # For India
USE_TZ = True
```

### Email Configuration (for future notifications)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Production Deployment Notes

1. Change SECRET_KEY to a random value
2. Set DEBUG = False
3. Add your domain to ALLOWED_HOSTS
4. Use environment variables for sensitive data
5. Set up HTTPS with SSL certificate
6. Use WhiteNoise for static files
7. Consider using Gunicorn + Nginx
8. Use PostgreSQL instead of MySQL for better reliability

## Support & Documentation

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- MySQL Documentation: https://dev.mysql.com/doc/

## Next Steps

1. Explore the admin panel at http://localhost:8000/admin
2. Create test accounts for patients and doctors
3. Set doctor working hours
4. Book and manage appointments
5. Customize styling by editing static/css files
6. Add more specializations or features as needed

---

**Happy Healthcare Management! 🏥**
