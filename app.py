from flask import Flask, render_template, request, redirect, url_for, session, send_file
import csv
import os
import json
from datetime import datetime
import subprocess
import threading
import time

app = Flask(__name__)
app.secret_key = "smart_attendance_secret_key"

ATT_FILE = "attendance.csv"

USERNAME = "DCME"
PASSWORD = "DCME155"

# Registration status tracking
registration_status = {"ongoing": False, "pin": "", "error": None}

# Load periods
with open("periods.json", "r") as f:
    periods_data = json.load(f)
    PERIODS = periods_data["periods"]

def read_attendance(date_filter=None, period_filter=None, pin_filter=None):
    records = []
    if not os.path.exists(ATT_FILE):
        return records

    with open(ATT_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            clean = {(k.strip().lower() if k else ""): (str(v).strip() if v else "") for k, v in row.items()}
            rec = {
                "ID": clean.get("id", ""),
                "PIN": clean.get("pin", ""),
                "Date": clean.get("date", ""),
                "Period": clean.get("period", "-"),
                "Time": clean.get("time", "")
            }

            if date_filter:
                if rec["Date"] != date_filter:
                    continue

            if period_filter and period_filter not in ("", "-", "all"):
                if str(rec["Period"]).strip() != str(period_filter).strip():
                    continue

            if pin_filter:
                if rec["PIN"] != pin_filter:
                    continue

            records.append(rec)

    records.sort(key=lambda r: (r["Date"], r["Period"], r["Time"]), reverse=True)
    return records

@app.route("/")
def home():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username", "").strip()
        p = request.form.get("password", "").strip()

        if u == USERNAME and p == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("menu"))
        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html", error=None)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    date_filter   = request.args.get("date",   "").strip() or None
    period_filter = request.args.get("period", "").strip()
    pin_filter    = request.args.get("pin",    "").strip() or None

    # "-" means "All Periods" — treat as no filter
    if period_filter in ("", "-"):
        period_filter = None

    records = read_attendance(
        date_filter=date_filter,
        period_filter=period_filter,
        pin_filter=pin_filter
    )

    today = datetime.now().strftime("%Y-%m-%d")

    all_records  = read_attendance()
    unique_pins  = sorted(set(r["PIN"] for r in all_records if r["PIN"]))

    return render_template(
        "dashboard_futuristic.html",
        records=records,
        selected_date=date_filter or "",
        selected_period=period_filter or "-",
        selected_pin=pin_filter or "",
        periods=PERIODS,
        unique_pins=unique_pins,
        today=today,
        total=len(records)
    )

@app.route("/download")
def download():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if not os.path.exists(ATT_FILE):
        return "attendance.csv not found", 404

    return send_file(ATT_FILE, as_attachment=True)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/menu")
def menu():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("menu.html")

@app.route("/register_student")
def register_student():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("register.html", error=None)

@app.route("/capture_faces", methods=["POST"])
def capture_faces():
    global registration_status
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    pin = request.form.get("pin", "").strip()
    
    if not pin:
        return render_template("register.html", error="PIN cannot be empty!")
    
    # Check if registration is already ongoing
    if registration_status["ongoing"]:
        return render_template("register.html", error="Registration already in progress. Please wait...")
    
    # Start registration in background thread
    registration_status["ongoing"] = True
    registration_status["pin"] = pin
    registration_status["error"] = None
    
    def run_registration_background():
        global registration_status
        try:
            subprocess.run(["python", "capturefaces.py", pin], check=True)
            run_training()
        except subprocess.CalledProcessError as e:
            registration_status["error"] = f"Face capture failed: {str(e)}"
        except Exception as e:
            registration_status["error"] = f"Error during registration: {str(e)}"
        finally:
            registration_status["ongoing"] = False
    
    thread = threading.Thread(target=run_registration_background, daemon=True)
    thread.start()
    
    # Return processing page
    return render_template("processing.html", pin=pin)

@app.route("/check_registration_status")
def check_registration_status():
    if not session.get("logged_in"):
        return {"status": "error", "message": "Not logged in"}, 401
    
    global registration_status
    if registration_status["ongoing"]:
        return {"status": "processing", "pin": registration_status["pin"]}
    elif registration_status["error"]:
        return {"status": "error", "message": registration_status["error"]}
    else:
        return {"status": "completed", "pin": registration_status["pin"]}

@app.route("/train_model")
def train_model():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    run_training()
    return redirect(url_for("menu"))

@app.route("/start_attendance")
def start_attendance():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    run_recognition()
    return redirect(url_for("menu"))

def run_training():
    subprocess.run(["python", "trainai.py"])

def run_recognition():
    subprocess.run(["python", "recogniseface.py"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
