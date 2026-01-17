from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = "very_secret_key_123"

# ===== PERMANENT LOGIN DETAILS =====
USERNAME = "admin"
PASSWORD = "admin123"

# ===== HOME ROUTE (PREVENTS 404) =====
@app.route("/")
def home():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

# ===== LOGIN ROUTE =====
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"

    return render_template_string("""
        <html>
        <head><title>Login</title></head>
        <body>
            <h2>Login</h2>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required><br><br>
                <input type="password" name="password" placeholder="Password" required><br><br>
                <button type="submit">Login</button>
            </form>
            <p style="color:red;">{{ error }}</p>
        </body>
        </html>
    """, error=error)

# ===== DASHBOARD =====
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return """
    <h1>Dashboard</h1>
    <p>You are logged in successfully ✅</p>
    <a href="/logout">Logout</a>
    """

# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ===== REQUIRED FOR RENDER =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
