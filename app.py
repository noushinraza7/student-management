
from flask import Flask, request
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.route("/")
def home():
    return """
    <h1>Student Management System</h1>
    <form action="/add" method="POST">
        <input name="name" placeholder="Student Name" required>
        <input name="email" placeholder="Student Email" required>
        <button type="submit">Add Student</button>
    </form>
    <a href="/students">View Students</a>
    """

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    email = request.form["email"]

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO students (name, email) VALUES (%s, %s)",
        (name, email)
    )

    db.commit()
    cursor.close()
    db.close()

    return "Student added successfully! <a href='/'>Go Back</a>"

@app.route("/students")
def students():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    cursor.close()
    db.close()

    output = "<h2>Registered Students</h2>"

    for student in records:
        output += f"<p>{student[1]} - {student[2]}</p>"

    return output

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
