from flask import Flask, render_template, request, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
DATA_FILE = "students.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)

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

        return "Registration submitted successfully!"

    return render_template("register.html")

@app.route("/admin")
def admin():
    students = load_students()
    return render_template("admin.html", students=students)

@app.route("/approve/<int:student_id>")
def approve(student_id):
    students = load_students()
    for s in students:
        if s["id"] == student_id:
            s["status"] = "approved"
    save_students(students)
    return redirect(url_for("admin"))

@app.route("/reject/<int:student_id>")
def reject(student_id):
    students = load_students()
    students = [s for s in students if s["id"] != student_id]
    save_students(students)
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run()
