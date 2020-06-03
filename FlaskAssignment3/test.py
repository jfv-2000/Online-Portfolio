import csv
from flask import Flask, render_template, url_for, redirect, request, flash
import bcrypt, string, random
from forms import ContactForm, SurveyForm, LoginForm, RegisterForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import sqlite3
from flask_sqlalchemy import SQLAlchemy

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

print('Random password : '+randomString())
