from flask import Flask, render_template, request, redirect, url_for, session, send_file
import csv
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "smart_attendance_secret_key")

ATT_FILE = "attendance.csv"

# Get credentials from environment variables (for security)
USERNAME = os.environ.get("ADMIN_USERNAME", "DCME")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "DCME155")

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
                "ID":     clean.get("id", ""),
                "PIN":    clean.get("pin", ""),
                "Date":   clean.get("date", ""),
                "Period": clean.get("period", "-"),
                "Time":   clean.get("time", "")
            }

            if date_filter:
                if rec["Date"] != date_filter:
                    continue

            if period_filter and period_filter not in ("", "-"):
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
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html", error=None)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    date_filter   = request.args.get("date",   "").strip() or None
    period_filter = request.args.get("period", "").strip()
    pin_filter    = request.args.get("pin",    "").strip() or None

    if period_filter in ("", "-"):
        period_filter = None

    records = read_attendance(
        date_filter=date_filter,
        period_filter=period_filter,
        pin_filter=pin_filter
    )
    today = datetime.now().strftime("%Y-%m-%d")

    all_records = read_attendance()
    unique_pins = sorted(set(r["PIN"] for r in all_records if r["PIN"]))

    return render_template(
        "dashboard_cloud.html",
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

@app.route("/health")
def health():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    # Create attendance.csv if it doesn't exist
    if not os.path.exists(ATT_FILE):
        with open(ATT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "PIN", "Date", "Period", "Time"])
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
