"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash, redirect, session

import hackbright

app = Flask(__name__)

app.secret_key = "this is secret stuff"

@app.route("/student-search")
def get_student_form():
    """"Show form for searching for a student"""

    return render_template("student_search.html")

@app.route("/new-student")
def get_new_student_form():
    """"Show form for creating a new student"""

    return render_template("new_student.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """add a student."""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    flash("New student was added!")
    return redirect(f"/student?github={github}")


@app.route("/project")
def show_project_info():
    """Show information about specific project"""

    title = request.args.get('title')

    title, description, max_grade = hackbright.get_project_by_title(title)
    rows = hackbright.get_student_grade_by_title(title)

    return render_template("project-info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           rows=rows)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')
    # print(hackbright.get_grades_by_github(github))
    first, last, github = hackbright.get_student_by_github(github)
    rows = hackbright.get_grades_by_github(github)

    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           rows=rows)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
