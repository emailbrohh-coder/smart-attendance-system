import cv2
import csv
from datetime import datetime
import os
import json
import numpy as np

# ---------------- FACE RECOGNIZER ----------------

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# ---------------- LOAD NAMES ----------------

names = {}
with open("names.txt", "r") as f:
    for line in f:
        if line.strip():
            uid, name = line.strip().split(",", 1)
            names[int(uid)] = name

# ---------------- LOAD PERIODS ----------------

with open("periods.json", "r") as f:
    periods_data = json.load(f)
    periods_list = periods_data["periods"]

def get_current_period():
    now = datetime.now()
    current_time = now.time()
    for period in periods_list:
        start = datetime.strptime(period["start"], "%H:%M").time()
        end   = datetime.strptime(period["end"],   "%H:%M").time()
        if start <= current_time < end:
            return period["number"]
    return "-"

# ---------------- CSV SETUP ----------------

ATT_FILE = "attendance.csv"

if not os.path.exists(ATT_FILE):
    with open(ATT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "PIN", "Date", "Period", "Time"])

def is_already_marked(uid, date, period):
    if not os.path.exists(ATT_FILE):
        return False
    with open(ATT_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get("ID", "").strip()     == str(uid) and
                row.get("Date", "").strip()   == date and
                row.get("Period", "").strip() == str(period)):
                return True
    return False

def mark_attendance(uid, pin):
    today  = datetime.now().strftime("%Y-%m-%d")
    period = get_current_period()

    if is_already_marked(uid, today, period):
        return False

    with open(ATT_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([uid, pin, today, period, datetime.now().strftime("%H:%M:%S")])

    print(f"✅ Attendance Marked: {pin} (Date: {today}, Period: {period})")
    return True

# ---------------- LIVENESS (OpenCV only) ----------------
# Uses Eye Aspect Ratio via eye cascade to detect blinks

EAR_CONSEC_FRAMES = 2   # frames eyes must be closed to count as blink
BLINK_REQUIRED    = 2   # blinks needed to confirm liveness

blink_counter   = 0
blink_total     = 0
liveness_confirmed = False

def check_eyes_open(face_roi_gray):
    """Returns True if eyes are detected (open), False if not (closed/blink)."""
    eyes = eye_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
    return len(eyes) >= 1

# ---------------- RECOGNITION SETTINGS ----------------

THRESHOLD      = 70
REQUIRED_STREAK = 3
last_uid        = None
streak          = 0
last_message_time   = 0
duplicate_alert_time = 0

# ---------------- CAMERA ----------------

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera not found. Check your camera connection.")
    exit(1)

print("📸 Smart Attendance Running... Press 'q' to quit.")
print("👁  Blink twice to confirm liveness, then hold still for attendance.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera read failed.")
        break

    h, w = frame.shape[:2]
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))
    current_time = datetime.now().timestamp()

    # ---- LIVENESS via eye blink detection ----
    if len(faces) > 0:
        x, y, fw, fh = faces[0]
        face_roi = gray[y:y+fh, x:x+fw]

        eyes_open = check_eyes_open(face_roi)

        if not eyes_open:
            blink_counter += 1
        else:
            if blink_counter >= EAR_CONSEC_FRAMES:
                blink_total += 1
                print(f"👁  Blink detected ({blink_total}/{BLINK_REQUIRED})")
            blink_counter = 0

        if blink_total >= BLINK_REQUIRED:
            liveness_confirmed = True

        status_text  = "LIVE ✅" if liveness_confirmed else f"Blink {BLINK_REQUIRED}x to verify ({blink_total}/{BLINK_REQUIRED})"
        status_color = (0, 255, 0) if liveness_confirmed else (0, 165, 255)
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
    else:
        liveness_confirmed = False
        blink_counter = 0
        cv2.putText(frame, "No face detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # ---- FACE RECOGNITION ----
    best_face       = None
    best_confidence = THRESHOLD
    best_uid        = None

    for (x, y, fw, fh) in faces:
        face_roi = gray[y:y+fh, x:x+fw]
        uid, confidence = recognizer.predict(face_roi)

        if confidence < best_confidence and uid in names:
            best_confidence = confidence
            best_uid        = uid
            best_face       = (x, y, fw, fh, uid, confidence)

    if best_face is not None:
        x, y, fw, fh, uid, confidence = best_face
        name = names[uid]

        if last_uid == uid:
            streak += 1
        else:
            last_uid = uid
            streak   = 1

        if streak >= REQUIRED_STREAK and liveness_confirmed:
            just_marked = mark_attendance(uid, name)
            if just_marked:
                last_message_time    = current_time
                duplicate_alert_time = 0
                # Reset liveness after marking
                blink_total        = 0
                liveness_confirmed = False
            else:
                duplicate_alert_time = current_time

        color = (0, 255, 0) if liveness_confirmed else (0, 165, 255)
        cv2.rectangle(frame, (x, y), (x+fw, y+fh), color, 2)
        cv2.putText(frame, f"{name} ({round(confidence, 1)})",
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    else:
        last_uid = None
        streak   = 0

    if current_time - last_message_time < 3:
        cv2.putText(frame, "✅ Attendance Marked!",
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    if current_time - duplicate_alert_time < 3:
        cv2.putText(frame, "Already marked this period!",
                    (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow("Smart Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
