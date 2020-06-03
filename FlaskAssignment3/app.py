from flask import Flask, render_template, url_for, redirect, request, flash, session
import bcrypt, string, random
from forms import ContactForm, SurveyForm, LoginForm, RegisterForm, ChangePasswordForm, ForgotPasswordForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
import sqlite3


app = Flask(__name__)
app.secret_key = 'secretkey'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config["USE_SESSION_FOR_NEXT"] = True

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEBUG'] = False
app.config['MAIL_USERNAME'] = 'jef.anhduc@gmail.com'
app.config['MAIL_PASSWORD'] = 'hzcntmmmyovpwumg'
app.config['MAIL_DEFAULT_SENDER'] = 'jef.anhduc@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False
mail = Mail()
mail.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/site.db'
db = SQLAlchemy(app)


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))


class ContactData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    message = db.Column(db.Text)


class SurveyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(50))


class User(UserMixin):
    def __init__(self, username, password=None):
        self.id = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    user = find_user(user_id)
    if user:
        user.password = None
    return user


def find_user(username):
    connection = sqlite3.connect('data/site.db')
    cur = connection.cursor()
    for row in cur.execute("SELECT username, password from user_data"):
        if not row:
            continue
        if username == row[0]:
            return User(row[0], row[1])
    return None


@app.route('/', methods=['GET', 'POST'])
def welcome():
    form = SurveyForm(request.form)
    if request.method == 'POST':
        if form.answer.data == 'r1':
            surveyInfo = SurveyData(answer="Social Medias")
            db.session.add(surveyInfo)
            db.session.commit()
        elif form.answer.data == 'r2':
            surveyInfo = SurveyData(answer="Networking Events")
            db.session.add(surveyInfo)
            db.session.commit()
        elif form.answer.data == 'r3':
            surveyInfo = SurveyData(answer="Other")
            db.session.add(surveyInfo)
            db.session.commit()
        else:
            flash("You must select an option to submit for the survey")
            return redirect(url_for('welcome'))
        return redirect(url_for('surveyResponse'))
    return render_template('home.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user(form.username.data)
        if user and bcrypt.checkpw(form.password.data.encode(), user.password):
            login_user(user)
            next_page = session.get('next', '/')
            session['next'] = '/'
            flash("log in successful")
            return redirect(next_page)
        flash('Wrong username or password')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash("Passwords must match")
            return redirect(url_for('register'))
        users = find_user(form.username.data)
        if not users:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode(), salt)
            userData = UserData(username=form.username.data, password=password)
            db.session.add(userData)
            db.session.commit()
            flash("Registration successful ! You can now log in")
            return redirect(url_for('login'))
        else:
            flash('This username already exists, please select another one.')
    return render_template('register.html', form=form)


@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SurveyForm(request.form)
    if request.method == 'POST':
        if form.answer.data == 'r1':
            surveyInfo = SurveyData(answer="Social Medias")
            db.session.add(surveyInfo)
            db.session.commit()
        elif form.answer.data == 'r2':
            surveyInfo = SurveyData(answer="Networking Events")
            db.session.add(surveyInfo)
            db.session.commit()
        elif form.answer.data == 'r3':
            surveyInfo = SurveyData(answer="Other")
            db.session.add(surveyInfo)
            db.session.commit()
        else:
            flash("You must select an option to submit for the survey")
            return redirect(url_for('welcome'))
        return redirect(url_for('surveyResponse'))
    return render_template('home.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contactMessage = ContactData(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(contactMessage)
        db.session.commit()
        msg = Message('Message from portfolio website', recipients=['jef.anhduc@gmail.com'])
        msg.body = "Name: " + form.name.data + "\nEmail: " + form.email.data + "\nMessage: " + form.message.data
        mail.send(msg)
        return redirect(url_for('contactResponse'))
    return render_template('contact.html', form=form)


@app.route('/contactResponse')
def contactResponse():
    return render_template('contactResponse.html')


@app.route('/surveyResponse')
def surveyResponse():
    return render_template('surveyResponse.html')


@app.route('/contactData')
@login_required
def contactData():
    contactInfo = []
    connection = sqlite3.connect('data/site.db')
    cur = connection.cursor()
    for row in cur.execute('SELECT * FROM contact_data'):
        contactInfo.append(row)
    return render_template('contactData.html', data=contactInfo)


@app.route('/surveyData')
@login_required
def surveyData():
    surveyInfo = []
    connection = sqlite3.connect('data/site.db')
    cur = connection.cursor()
    for row in cur.execute('SELECT * FROM survey_data'):
        surveyInfo.append(row)
    return render_template('surveyData.html', data=surveyInfo)


@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if form.newPassword.data != form.newPassword2.data:
            flash("Passwords must match")
            return redirect(url_for('changePassword'))
        connection = sqlite3.connect('data/site.db')
        cur = connection.cursor()
        for row in cur.execute("SELECT username, password from user_data"):
            if(current_user.id == row[0]):
                presentPassword = row[1]
                if bcrypt.checkpw(form.currentPassword.data.encode(), presentPassword):
                    id = current_user.id
                    salt = bcrypt.gensalt()
                    newPassword = bcrypt.hashpw(form.newPassword2.data.encode(), salt)
                    cur.execute("Update user_data set password=? where username=?", (newPassword, id))
                    connection.commit()
                    cur.close()
                    logout_user()
                    flash("You have been logged out. Your password has been changed !")
                    return redirect('/')
                else:
                    flash("Wrong Password")
                    return redirect('/changePassword')
    return render_template('changePassword.html', form=form)


def generateRandomPassword(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        connection = sqlite3.connect('data/site.db')
        cur = connection.cursor()
        for row in cur.execute("SELECT username, password from user_data"):
            if form.username.data == row[0]:
                flash("A new password has been sent to your email so you can reset your password !")
                resetPassword = generateRandomPassword()
                salt = bcrypt.gensalt()
                newResetPassword = bcrypt.hashpw(resetPassword.encode(), salt)
                username = form.username.data
                cur.execute("Update user_data set password=? where username=?", (newResetPassword, username))
                connection.commit()
                cur.close()
                msg = Message('Forgot Password from Jean-Francois Website', recipients=[form.username.data])
                msg.body = "Your password has been reset. Your new password is now : "+resetPassword+"\nYou can change your password with it."
                mail.send(msg)
                return redirect('/login')
        flash("There is no account associated with that email. ")
        return redirect('/forgotPassword')
    return render_template('forgotPassword.html', form=form)


if __name__ == '__main__':
    app.run()
