from dashboard import db, login_manager
from dashboard import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        # password encryption logic
        self.password_hash = bcrypt.generate_password_hash(plain_text_password)

    # return unhashed password
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


student_course = db.Table('student_course',
                          db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                          db.Column('course_id', db.Integer, db.ForeignKey('course.id')))

instructor_course = db.Table('instructor_course',
                             db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id')),
                             db.Column('course_id', db.Integer, db.ForeignKey('course.id')))


class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    course_ID = db.Column(db.String(length=20), nullable=False)
    instructor_ID = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    course_location = db.Column(db.String(length=1024), nullable=False, unique=True)
    registration_status = db.Column(db.String(length=10), nullable=False)
    # takers = db.Column(db.Integer(), db.ForeignKey('student.id'))
    # teachers = db.Column(db.Integer(), db.ForeignKey('instructor.id'))

    def __repr__(self):
        return f'Course {self.name}'


class Student(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=1024), nullable=False)
    gender = db.Column(db.String(length=10), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    major = db.Column(db.String(length=1024), nullable=False)
    email = db.Column(db.String(length=1024), nullable=False)
    studentID = db.Column(db.Integer(), nullable=False)
    courses_taking = db.relationship('Course', secondary=student_course, backref='takers')

    def __repr__(self):
        return f'Student {self.name}'


class Instructor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=1024), nullable=False)
    gender = db.Column(db.String(length=10), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(length=1024), nullable=False)
    courses_teaching = db.relationship('Course', secondary=instructor_course, backref='teachers')
