# Guardian Angels - Deployment Guide

This guide helps you host the Guardian Angels web application on GitHub and deploy it to a live server.

## Option 1: Railway (Recommended) ⭐ - FREE & EASIEST

Railway is perfect for Django apps and supports up to 500 free hours/month.

### Step 1: Push to GitHub
1. Create a new repository on [GitHub](https://github.com/new)
2. In your project directory, run:
```bash
git init
git add .
git commit -m "Initial commit: Guardian Angels"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/guardian-angels.git
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `guardian-angels` repository
5. Railway automatically detects Django (Procfile) and deploys

### Step 3: Configure Environment Variables
In Railway dashboard:
- Add `SECRET_KEY`: Generate a new one
- Add `DEBUG`: Set to `False`
- Add `ALLOWED_HOSTS`: Your Railway domain (e.g., `yourdomain.railway.app`)

### Database Setup on Railway
- Railway provides PostgreSQL for free
- Update `settings.py` to use PostgreSQL
- Run migrations: `python manage.py migrate`

---

## Option 2: Heroku (Free tier requirements changed)

Heroku's free tier is limited. Use if you have credits.

```bash
# Install Heroku CLI, then:
heroku login
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

---

## Option 3: Render.com

1. Sign up at [Render.com](https://render.com)
2. Create Web Service from GitHub
3. Select your repository
4. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
5. Start command: `gunicorn guardian_angels.wsgi`
6. Add environment variables (same as Railway)

---

## Before Deployment - Important!

### 1. Update Settings.py for Production
```python
# guardian_angels/settings.py

import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# For Railway/Heroku with PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PGDATABASE', default='postgres'),
        'USER': config('PGUSER', default='postgres'),
        'PASSWORD': config('PGPASSWORD', default=''),
        'HOST': config('PGHOST', default='localhost'),
        'PORT': config('PGPORT', default='5432'),
    }
}

# Static files (WhiteNoise handles these)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 2. Handle Database Migration

Since your current app uses MySQL/SQLite, you'll need to migrate to PostgreSQL:
1. Export current data (optional but recommended)
2. Deploy to Railway/Render
3. Run: `python manage.py migrate` on the platform
4. Re-create demo data if needed

### 3. Generate Security Key
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## Full Deployment Steps

1. **Prepare locally:**
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   ```

2. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Ready for deployment"
   git push -u origin main
   ```

3. **Deploy to Railway:**
   - Connect GitHub account
   - Select repository
   - Wait for automatic deployment
   - Configure environment variables
   - Run migrations in Railway shell

4. **Access your app:**
   - URL format: `https://yourapp.railway.app`
   - Share with third parties!

---

## Troubleshooting

**"Static files not loading"**
- Run: `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` and `STATIC_URL` in settings

**"Database connection error"**
- Verify DATABASE env vars match your hosting provider
- Ensure database is running

**"Module not found"**
- Ensure all packages in `requirements.txt` are installed
- Check Python version matches `runtime.txt`

**"CSRF token missing"**
- Ensure `CSRF_TRUSTED_ORIGINS` includes your domain
- Check cookies are enabled

---

## Current Project Status

✅ `.gitignore` - Created to exclude sensitive files
✅ `Procfile` - Ready for Heroku/Railway
✅ `runtime.txt` - Python 3.11.7
✅ `requirements.txt` - Updated with production dependencies
✅ `wsgi.py` - Configured with WhiteNoise

Your project is ready to push to GitHub and deploy!
