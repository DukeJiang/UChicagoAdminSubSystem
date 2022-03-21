from dashboard import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from dashboard.models import Course, User, Student, Instructor
from dashboard.forms import RegisterForm, LoginForm, AddCourseForm, AddStudentForm
from dashboard import db
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/courses')
@login_required
def courses_page():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


@app.route('/students')
@login_required
def students_page():
    students = Student.query.all()
    return render_template('students.html', students=students)


# register API, handles account registration post request
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # flask invokes builder pattern
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)  # pass in password to call password setter method for encryption
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('courses_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    # users will be served this page when they are directed to /register
    # pass in form as a form obj
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # query through the database and find if there is a username present
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('courses_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course_page():
    form = AddCourseForm()
    if form.validate_on_submit():
        # leverages builder pattern
        course_to_create = Course(name=form.name.data,
                                  course_ID=form.course_ID.data,
                                  instructor_ID=int(form.instructor_ID.data),
                                  course_location=form.course_location.data,
                                  description=form.description.data,
                                  registration_status="OPEN")
        db.session.add(course_to_create)
        db.session.commit()
        flash(f"Course with ID {course_to_create.course_ID} has been created)", category='success')
        return redirect(url_for('courses_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('add_course.html', form=form)


@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student_page():
    form = AddStudentForm()
    if form.validate_on_submit():
        student_to_create = Student(name=form.name.data,
                                    gender=form.gender.data,
                                    age=form.age.data,
                                    major=form.major.data,
                                    email=form.email.data,
                                    studentID=form.studentID.data)
        db.session.add(student_to_create)
        db.session.commit()
        flash(f"Student with ID {student_to_create.studentID} has been created)", category='success')
        return redirect(url_for('students_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('add_student.html', form=form)


@app.route('/change_student_info/<int:student_id>', methods=['GET', 'POST'])
@login_required
def change_student_info(student_id):
    form = AddStudentForm()
    if form.validate_on_submit():
        changed_info = Student(name=form.name.data,
                               gender=form.gender.data,
                               age=form.age.data,
                               major=form.major.data,
                               email=form.email.data,
                               studentID=form.studentID.data)
        original_student = Student.query.filter_by(id=student_id).first()
        db.session.delete(original_student)
        db.session.add(changed_info)
        db.session.commit()
        flash(f"Student with ID {changed_info.studentID} has been changed)", category='success')
        return redirect(url_for('students_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('change_student.html', form=form)


@app.route('/student_roster/<int:course_id>', methods=['GET', 'POST'])
def student_roster_page(course_id):
    target_course = Course.query.filter_by(id=course_id).first()
    students = target_course.takers
    return render_template('student_roster.html', students=students)


@app.route('/close_registration/<int:course_id>', methods=['GET', 'POST'])
def close_registration(course_id):
    target_course = Course.query.filter_by(id=course_id).first()
    target_course.registration_status = "CLOSED"
    db.session.commit()
    return redirect(url_for('courses_page'))


@app.route('/delete_course/<int:course_id>', methods=['GET', 'POST'])
def delete_course(course_id):
    target_course = Course.query.filter_by(id=course_id).first()
    db.session.delete(target_course)
    db.session.commit()
    return redirect(url_for('courses_page'))


@app.route('/delete_student/<int:student_id>', methods=['GET', 'POST'])
def delete_student(student_id):
    target_student = Student.query.filter_by(id=student_id).first()
    db.session.delete(target_student)
    db.session.commit()
    return redirect(url_for('students_page'))
