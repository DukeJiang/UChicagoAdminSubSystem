from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from dashboard.models import User


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

    def validate_username(self, username_to_check):
        # query through the database and check if the passed in username already exists
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class AddCourseForm(FlaskForm):
    name = StringField(label='Course Name:', validators=[DataRequired()])
    course_ID = StringField(label='Course ID:', validators=[DataRequired()])
    instructor_ID = StringField(label='Instructor ID:', validators=[DataRequired()])
    course_location = StringField(label='Course Location:', validators=[DataRequired()])
    description = StringField(label='Description:', validators=[DataRequired()])
    submit = SubmitField(label='Create Course')


class AddStudentForm(FlaskForm):
    name = StringField(label='Student Name:', validators=[DataRequired()])
    gender = StringField(label='Gender:', validators=[DataRequired()])
    age = StringField(label='Student Name:', validators=[DataRequired()])
    major = StringField(label='Student Name:', validators=[DataRequired()])
    email = StringField(label='Student Name:', validators=[DataRequired()])
    studentID = StringField(label='Student Name:', validators=[DataRequired()])
    submit = SubmitField(label='Add Student')