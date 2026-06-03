from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import subprocess
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "gesture123"


# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        # ✅ CHECK IF USER EXISTS
        if not user:
            flash("New user? Please create an account on Register page.")
            return redirect(url_for("register"))

        # ✅ CHECK PASSWORD
        elif not check_password_hash(user[2], password):
            flash("Incorrect password! Please try again.")
            return redirect(url_for("login"))

        # ✅ SUCCESS
        else:
            session["user"] = username
            return redirect(url_for("instruction"))

    return render_template("login.html")


# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users(username, password) VALUES(?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            flash("Registration Successful! Please login.")
            return redirect(url_for("login"))
        except:
            flash("Username already exists!")
            return redirect(url_for("register"))

    return render_template("register.html")


# ---------- INSTRUCTION ----------
@app.route("/instruction")
def instruction():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("instruction.html")


# ---------- START ----------
@app.route("/start")
def start():
    if "user" not in session:
        return redirect(url_for("login"))

    subprocess.Popen(["python", "mouse_control.py"])
    return "<h2>Gesture Virtual Mouse Started.<br>Press 'Q' to stop.</h2>"


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)