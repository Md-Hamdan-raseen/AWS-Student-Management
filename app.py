from flask import Flask, render_template, request, redirect
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)


# MySQL database connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()


# Home page - Display students
@app.route("/")
def index():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    return render_template("index.html", students=students)


# Add student
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        age = request.form["age"]

        sql = """
        INSERT INTO students (name, email, course, age)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (name, email, course, age))
        db.commit()

        return redirect("/")

    return render_template("add_student.html")


# Edit student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        age = request.form["age"]

        sql = """
        UPDATE students
        SET name=%s, email=%s, course=%s, age=%s
        WHERE id=%s
        """

        cursor.execute(
            sql,
            (name, email, course, age, id)
        )

        db.commit()

        return redirect("/")

    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (id,)
    )

    student = cursor.fetchone()

    return render_template(
        "edit_student.html",
        student=student
    )


# Delete student
@app.route("/delete/<int:id>")
def delete_student(id):

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect("/")


# Start Flask application
if __name__ == "__main__":
    app.run(debug=True)