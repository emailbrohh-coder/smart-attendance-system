import os
import subprocess

def run_capture():
    subprocess.run(["python", "capturefaces.py"])

def run_training():
    subprocess.run(["python", "trainai.py"])

def run_recognition():
    subprocess.run(["python", "recogniseface.py"])

def run_dashboard():
    subprocess.run(["python", "app.py"])

while True:
    print("\n===== SMART ATTENDANCE SYSTEM =====")
    print("1. Register New Student (Capture Face)")
    print("2. Train Face Recognition Model")
    print("3. Start Attendance System")
    print("4. Open Attendance Dashboard")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        run_capture()
        print("\nTraining Face Recognition Model...")
        run_training()
        print("Training complete.")
    elif choice == "2":
        run_training()
    elif choice == "3":
        run_recognition()
    elif choice == "4":
        run_dashboard()
    elif choice == "5":
        print("Exiting System...")
        break
    else:
        print("Invalid choice. Try again.")
