from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')


class SurveyForm(FlaskForm):
    answer = RadioField('Answers', validators=[DataRequired()],
                        choices=[('r1', 'Social Medias'), ('r2', 'Networking Events'), ('r3', 'Other')], render_kw={'required': True})
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = EmailField('Username', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    enter = SubmitField('Enter')


class RegisterForm(FlaskForm):
    username = EmailField('Username', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[InputRequired()], render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat password', validators=[InputRequired()], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')


class ChangePasswordForm(FlaskForm):
    currentPassword = PasswordField('Password', validators=[InputRequired()],
                                    render_kw={"placeholder": "Current Password"})
    newPassword = PasswordField('Password', validators=[InputRequired()], render_kw={"placeholder": "New Password"})
    newPassword2 = PasswordField('Repeat password', validators=[InputRequired()],
                                 render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Confirm')


class ForgotPasswordForm(FlaskForm):
    username = EmailField('Username', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    enter = SubmitField('Enter')
