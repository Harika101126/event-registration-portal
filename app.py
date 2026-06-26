from flask import Flask, render_template, request, redirect, session, Response
import sqlite3
import csv
import io

app = Flask(__name__)
app.secret_key = "harika_event_secret"

def create_table():
    conn = sqlite3.connect("event.db")
    cursor = conn.cursor()

    # registrations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        college TEXT,
        year TEXT,
        registration_date TEXT
    )
    """)

    # event settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS event_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        subtitle TEXT,
        event_date TEXT,
        event_time TEXT,
        venue TEXT
    )
    """)

    # insert default event only if table is empty
    cursor.execute("SELECT COUNT(*) FROM event_settings")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
        INSERT INTO event_settings
        (title, subtitle, event_date, event_time, venue)
        VALUES (?, ?, ?, ?, ?)
        """, (
            "TechFest 2026",
            "Join developers, innovators and tech enthusiasts for an exciting technology event.",
            "26 July 2026",
            "10:00 AM",
            "Annamacharya University"
        ))

    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect("event.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM event_settings WHERE id=1")
    event = cursor.fetchone()

    conn.close()

    return render_template("index.html", event=event)

@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    college = request.form["college"]
    year = request.form["year"]

    conn = sqlite3.connect("event.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO registrations
    (name,email,phone,college,year,registration_date)
    VALUES (?,?,?,?,?,datetime('now'))
    """, (name,email,phone,college,year))

    conn.commit()
    conn.close()

    return render_template("success.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["admin_logged_in"] = True
            return redirect("/admin")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")
@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    conn = sqlite3.connect("event.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM registrations")
    data = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM registrations")
    total = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        data=data,
        total=total
    )
@app.route("/edit-event", methods=["GET", "POST"])
def edit_event():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    conn = sqlite3.connect("event.db")
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        event_date = request.form["event_date"]
        event_time = request.form["event_time"]
        venue = request.form["venue"]

        cursor.execute("""
        UPDATE event_settings
        SET title=?, subtitle=?, event_date=?, event_time=?, venue=?
        WHERE id=1
        """, (title, subtitle, event_date, event_time, venue))

        conn.commit()
        conn.close()

        return redirect("/admin")

    cursor.execute("SELECT * FROM event_settings WHERE id=1")
    event = cursor.fetchone()

    conn.close()

    return render_template("edit_event.html", event=event)
@app.route("/export-csv")
def export_csv():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    conn = sqlite3.connect("event.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, phone, college, year, registration_date
        FROM registrations
    """)
    data = cursor.fetchall()

    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    # CSV header
    writer.writerow(["ID", "Name", "Email", "Phone", "College", "Year", "Registration Date"])

    # CSV rows
    for row in data:
        writer.writerow(row)

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=registrations.csv"}
    )
@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("admin_logged_in"):
      return redirect("/login")

    conn = sqlite3.connect("event.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM registrations WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")
@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect("/login")

create_table()

if __name__ == "__main__":
    create_table()
    app.run(host="0.0.0.0", port=5000, debug=True)