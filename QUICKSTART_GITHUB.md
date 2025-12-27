# Quick Start Guide for GitHub & Deployment

## 1️⃣ Initialize Git Locally (Windows PowerShell)

```powershell
cd "c:\Users\Arnab Basu Roy\OneDrive\Desktop\arpan\Guardian Angels VS\guardian_angels"

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Guardian Angels appointment booking system"

# Rename branch to main
git branch -M main
```

## 2️⃣ Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Create repository named: `guardian-angels`
3. **DO NOT** initialize with README (you have one)
4. Click "Create repository"
5. Copy the HTTPS URL (will look like: `https://github.com/YOUR_USERNAME/guardian-angels.git`)

## 3️⃣ Push to GitHub (PowerShell)

```powershell
cd "c:\Users\Arnab Basu Roy\OneDrive\Desktop\arpan\Guardian Angels VS\guardian_angels"

# Add remote origin
git remote add origin https://github.com/YOUR_USERNAME/guardian-angels.git

# Push to GitHub
git push -u origin main

# You'll be prompted for credentials - use your GitHub token or password
```

## 4️⃣ Deploy to Railway (Free, Recommended)

1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize GitHub and select `guardian-angels`
5. Railway auto-deploys! (may take 2-5 minutes)
6. Once deployed, you'll get a URL like: `https://yourapp-prod.up.railway.app`

## 5️⃣ Configure Production Settings

You'll need to update `guardian_angels/settings.py` for the live environment.

**Key changes needed:**
- Change `DEBUG = True` to `DEBUG = False` (or use env variables)
- Update `ALLOWED_HOSTS` with your Railway domain
- Configure PostgreSQL (Railway provides free PostgreSQL)

See [DEPLOYMENT.md](DEPLOYMENT.md) for full settings.py example.

## 6️⃣ Share Your Live Site

- Anyone with your Railway URL can access your website
- Example: `https://guardian-angels-prod.up.railway.app`
- Works on any device (phone, tablet, other computers)

---

## Troubleshooting Commands

```powershell
# Check git status
git status

# View commit history
git log --oneline

# Check remote
git remote -v

# Pull latest changes (if working with team)
git pull origin main

# Push new changes
git add .
git commit -m "Your message"
git push origin main
```

---

## What Files Were Added/Modified?

✅ `.gitignore` - Prevents pushing sensitive files
✅ `Procfile` - Tells Railway how to run the app
✅ `runtime.txt` - Specifies Python version
✅ `requirements.txt` - Added production dependencies (gunicorn, whitenoise)
✅ `wsgi.py` - Updated for production
✅ `DEPLOYMENT.md` - Full deployment documentation

**Your code is NOT modified** - these are just configuration files for hosting!
