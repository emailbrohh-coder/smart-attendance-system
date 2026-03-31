import cv2
import os
import sys

# ---------- SETTINGS ----------
SAMPLES = 50
DATASET_DIR = "dataset"
NAMES_FILE = "names.txt"
# -----------------------------

os.makedirs(DATASET_DIR, exist_ok=True)

def get_next_id():
    """Returns next available user id by reading names.txt"""
    if not os.path.exists(NAMES_FILE):
        return 1

    max_id = 0
    with open(NAMES_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                uid = int(line.split(",")[0])
                max_id = max(max_id, uid)
            except:
                pass
    return max_id + 1

user_id = get_next_id()

# Accept PIN from command-line argument or prompt for it
if len(sys.argv) > 1:
    pin = sys.argv[1].strip()
else:
    pin = input("Enter PIN for new user: ").strip()

print(f"✅ New Person ID = {user_id}, PIN = {pin}")
print("Look at camera... capturing samples... Press 'q' to stop early.")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera not working")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face_img = gray[y:y+h, x:x+w]
        file_path = f"{DATASET_DIR}/User.{user_id}.{count}.jpg"
        cv2.imwrite(file_path, face_img)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{user_id}  Samples:{count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Capture Faces", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if count >= SAMPLES:
        break

cap.release()
cv2.destroyAllWindows()

# Save name mapping WITHOUT overwriting
with open(NAMES_FILE, "a") as f:
    f.write(f"{user_id},{pin}\n")

print(f"✅ Done! Saved {count} samples for PIN {pin} (ID {user_id})")
