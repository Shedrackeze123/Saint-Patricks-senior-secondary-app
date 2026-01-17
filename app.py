from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Registration</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            padding: 20px;
        }
        form {
            background: white;
            padding: 20px;
            max-width: 400px;
            margin: auto;
            border-radius: 8px;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
        }
        button {
            background: green;
            color: white;
            border: none;
        }
    </style>
</head>
<body>
    <h2 align="center">Saint Patrick's Senior Secondary School</h2>

    <form method="POST">
        <input type="text" name="fullname" placeholder="Full Name" required>
        
        <select name="class" required>
            <option value="">Select Class</option>
            <option>JSS 1</option>
            <option>JSS 2</option>
            <option>JSS 3</option>
            <option>SS 1</option>
            <option>SS 2</option>
            <option>SS 3</option>
        </select>

        <select name="gender" required>
            <option value="">Gender</option>
            <option>Male</option>
            <option>Female</option>
        </select>

        <input type="date" name="dob" required>

        <button type="submit">Register</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        student_class = request.form["class"]
        gender = request.form["gender"]
        dob = request.form["dob"]

        with open("students.txt", "a") as f:
            f.write(f"{fullname}, {student_class}, {gender}, {dob}\n")

        return "<h3 align='center'>Registration Successful ✅</h3>"

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run()
