from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

# PERMANENT LOGIN DETAILS
USERNAME = "admin"
PASSWORD = "admin123"


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "❌ Invalid login", 401

    return """
    <h2>Login</h2>
    <form method="post">
        <input name="username" placeholder="Username" required><br><br>
        <input name="password" type="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    """


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return """
    <h1>Dashboard</h1>
    <p>Login successful ✅</p>
    <a href="/logout">Logout</a>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
