# 📸 Smart Attendance System

Face recognition-based attendance system with cloud dashboard access.

## 🌟 Features

- **Face Recognition**: LBPH algorithm with OpenCV
- **Anti-Spoofing**: Blink detection + head movement verification using MediaPipe
- **Period-Based Tracking**: Automatic period detection (7 periods)
- **Cloud Dashboard**: View attendance from anywhere
- **CSV Export**: Download attendance records
- **Duplicate Prevention**: Won't mark same student twice in same period

## 🏗️ Architecture

- **Local System**: Face capture, training, and recognition (requires camera)
- **Cloud Dashboard**: Web interface for viewing/downloading records (accessible anywhere)

## 🚀 Quick Start

### Local Setup (Face Recognition)

1. Install dependencies:
```bash
pip install opencv-python opencv-contrib-python mediapipe pillow numpy flask
```

2. Run the system:
```bash
python main.py
```

3. Choose from menu:
   - Register new student (capture face)
   - Train model
   - Start attendance
   - Open local dashboard

### Cloud Deployment (Dashboard Only)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Quick steps:**
1. Push code to GitHub
2. Deploy to Render (free)
3. Access dashboard from anywhere

## 📁 Project Structure

```
├── app.py                  # Local Flask app (full features)
├── app_cloud.py           # Cloud Flask app (dashboard only)
├── main.py                # CLI menu system
├── capturefaces.py        # Face capture module
├── trainai.py             # Model training
├── recogniseface.py       # Live attendance with anti-spoofing
├── attendance.csv         # Attendance records
├── names.txt              # Student ID to PIN mapping
├── periods.json           # Period timings
├── dataset/               # Face images (50 per student)
├── trainer/               # Trained model (trainer.yml)
├── templates/             # HTML templates
└── static/                # CSS files
```

## 🔄 Syncing Data to Cloud

After marking attendance locally, sync to cloud:

```bash
python sync_to_cloud.py
```

Or manually:
```bash
git add attendance.csv
git commit -m "Update attendance"
git push
```

## 🎓 Student Registration

1. Run: `python capturefaces.py` or use menu option 1
2. Enter student PIN (e.g., 23155-CM-067)
3. Look at camera - system captures 50 samples
4. Train model: `python trainai.py`
5. Student ready for attendance!

## ✅ Taking Attendance

1. Run: `python recogniseface.py` or use menu option 3
2. Students look at camera
3. System verifies liveness (blink 3x + move head)
4. Attendance marked automatically
5. Prevents duplicates in same period

## 🔐 Default Credentials

**Username**: DCME  
**Password**: DCME155

⚠️ Change these in production! Edit in `app.py` or use environment variables.

## 📊 Dashboard Features

- Filter by date, period, and student PIN
- View all attendance records
- Download CSV export
- Real-time statistics
- Mobile-friendly interface

## 🛠️ Technologies

- **Backend**: Flask (Python)
- **Face Recognition**: OpenCV + LBPH
- **Liveness Detection**: MediaPipe
- **Frontend**: HTML/CSS/JavaScript
- **Storage**: CSV (upgradeable to database)
- **Deployment**: Render (free tier)

## 📝 Period Configuration

Edit `periods.json` to customize period timings:

```json
{
  "periods": [
    {"number": 1, "name": "Period 1", "start": "07:00", "end": "10:50"},
    ...
  ]
}
```

## 🔧 Troubleshooting

**Camera not working:**
- Check camera permissions
- Try different camera index in code (0, 1, 2)

**Face not detected:**
- Ensure good lighting
- Face camera directly
- Remove glasses/masks if needed

**Model accuracy low:**
- Capture more samples (increase SAMPLES in capturefaces.py)
- Retrain model with better lighting
- Ensure diverse angles during capture

**Cloud dashboard not updating:**
- Run `python sync_to_cloud.py`
- Check git remote is configured
- Verify Render deployment succeeded

## 📞 Support

For deployment help, see [DEPLOYMENT.md](DEPLOYMENT.md)

## 📄 License

Educational project for Govt Polytechnic Pillaripattu

---

Made with ❤️ for smart attendance tracking
