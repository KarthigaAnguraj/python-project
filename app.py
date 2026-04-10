from flask import Flask, render_template, request, redirect
import sqlite3
import os
app = Flask(__name__)

# Upload folder (for future image upload)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # Reports table
    c.execute("""
    CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        location TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO users(username, password) VALUES(?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            return redirect('/report')
        else:
            return "Invalid Login ❌"

    return render_template('login.html')

# ---------------- REPORT ----------------
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        username = request.form['username']
        location = request.form['location']

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO reports(username, location, status) VALUES(?, ?, ?)",
                     (username, location, "Reported"))
        conn.commit()
        conn.close()

        return redirect('/report')

    return render_template('report.html')

# ---------------- ADMIN ----------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        report_id = request.form['id']
        status = request.form['status']

        cur.execute("UPDATE reports SET status=? WHERE id=?", (status, report_id))
        conn.commit()

    cur.execute("SELECT * FROM reports")
    reports = cur.fetchall()
    conn.close()

    return render_template('admin.html', reports=reports)


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)