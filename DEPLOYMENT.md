# 🌐 Smart Attendance System - Cloud Deployment Guide

## Architecture Overview

This system uses a **hybrid architecture**:
- **Cloud (Render)**: Web dashboard for viewing/downloading attendance records
- **Local**: Face capture, training, and recognition (requires camera access)

## 📋 Prerequisites

1. GitHub account
2. Render account (free tier) - https://render.com
3. Git installed on your computer

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

1. Initialize git in your project folder:
```bash
git init
git add .
git commit -m "Initial commit - Smart Attendance System"
```

2. Create a new repository on GitHub (https://github.com/new)
   - Name it: `smart-attendance-system`
   - Keep it public or private (your choice)
   - Don't initialize with README

3. Push your code to GitHub:
```bash
git remote add origin https://github.com/YOUR_USERNAME/smart-attendance-system.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Render

1. Go to https://render.com and sign up/login

2. Click **"New +"** → **"Web Service"**

3. Connect your GitHub repository:
   - Click "Connect account" if first time
   - Select your `smart-attendance-system` repository

4. Configure the service:
   - **Name**: `smart-attendance-dashboard`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app_cloud:app`
   - **Instance Type**: `Free`

5. Add Environment Variables (click "Advanced"):
   - `SECRET_KEY` = `your-random-secret-key-here-change-this`
   - `ADMIN_USERNAME` = `DCME` (or your preferred username)
   - `ADMIN_PASSWORD` = `DCME155` (or your preferred password)

6. Click **"Create Web Service"**

7. Wait 5-10 minutes for deployment to complete

8. Your dashboard will be live at: `https://smart-attendance-dashboard.onrender.com`

### Step 3: Sync Attendance Data

Since face recognition runs locally, you need to sync the `attendance.csv` file to the cloud.

**Option A: Manual Upload (Simple)**
1. Use Render's Shell feature to upload files
2. Or use Git to commit and push attendance.csv updates

**Option B: Automated Sync (Recommended)**
Use a cloud storage service like:
- Google Drive API
- Dropbox API
- AWS S3 (free tier)

Both local and cloud apps read/write to the same CSV file in cloud storage.

### Step 4: Run Local System

On your local computer with camera:

```bash
python main.py
```

Or run individual components:
- Register student: `python capturefaces.py`
- Train model: `python trainai.py`
- Start attendance: `python recogniseface.py`

## 🔄 Syncing Data Between Local and Cloud

### Quick Solution: Git-based Sync

After attendance is marked locally:

```bash
git add attendance.csv
git commit -m "Update attendance"
git push
```

Render will auto-deploy and update the dashboard.

### Better Solution: Shared Database

Replace CSV with a cloud database:
- **PostgreSQL** (Render provides free tier)
- **MongoDB Atlas** (free tier)
- **Supabase** (free tier with PostgreSQL)

This allows real-time sync between local and cloud.

## 🔒 Security Notes

1. **Change default credentials** in environment variables
2. **Use HTTPS** (Render provides this automatically)
3. **Don't commit** sensitive data to GitHub:
   - Add `.env` to `.gitignore`
   - Use environment variables for secrets

## 📱 Accessing Your Dashboard

Once deployed, you can access from anywhere:
- Desktop: `https://your-app-name.onrender.com`
- Mobile: Same URL works on phones/tablets
- Share with teachers/admins

## 💡 Free Tier Limitations

**Render Free Tier:**
- App sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds (cold start)
- 750 hours/month (enough for most use cases)

**Solutions:**
- Use a uptime monitor (UptimeRobot) to ping every 14 minutes
- Upgrade to paid tier ($7/month) for always-on service

## 🆘 Troubleshooting

**Build fails:**
- Check `requirements.txt` has correct package versions
- View build logs in Render dashboard

**App crashes:**
- Check application logs in Render
- Ensure `attendance.csv` exists (app creates it automatically)

**Can't login:**
- Verify environment variables are set correctly
- Check username/password match

## 📞 Need Help?

Check Render documentation: https://render.com/docs
