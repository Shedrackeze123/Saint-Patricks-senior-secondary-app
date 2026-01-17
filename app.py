from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 🔐 REQUIRED for login sessions
app.secret_key = "change_this_secret_key_later"

# 🔐 PERMANENT ADMIN CREDENTIALS (FROM RENDER)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

UPLOAD_FOLDER = "static/uploads"
DATA_FILE = "students.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------- HELPERS -----------------
def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)

# ----------------- STUDENT REGISTRATION -----------------
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        students = load_students()

        photo = request.files["photo"]
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(photo_path)

        student = {
            "id": len(students) + 1,
            "name": request.form["name"],
            "phone": request.form["phone"],
            "photo": photo_path,
            "status": "pending"
        }

        students.append(student)
        save_students(students)

        return "Registration submitted successfully! Awaiting approval."

    return render_template("register.html")

# ----------------- ADMIN LOGIN -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))

        return "Wrong username or password!"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

# ----------------- ADMIN PANEL -----------------
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))

    students = load_students()
    return render_template("admin.html", students=students)

@app.route("/approve/<int:student_id>")
def approve(student_id):
    if not session.get("admin"):
        return redirect(url_for("login"))

    students = load_students()
    for s in students:
        if s["id"] == student_id:
            s["status"] = "approved"

    save_students(students)
    return redirect(url_for("admin"))

@app.route("/reject/<int:student_id>")
def reject(student_id):
    if not session.get("admin"):
        return redirect(url_for("login"))

    students = load_students()
    students = [s for s in students if s["id"] != student_id]
    save_students(students)

    return redirect(url_for("admin"))

# ----------------- RUN -----------------
if __name__ == "__main__":
    app.run()
