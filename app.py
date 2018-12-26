import os
from flask import Flask, render_template, url_for, flash, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


app = Flask(__name__)
bootstrap = Bootstrap(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config['SECRET_KEY'] = 'gs33sg34!pinndgSD45%lObN'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cezykxbcbwguds:ce990760be16388bf589436f85c415dae80eb7680b97ce724c2efd3e363fe04e@ec2-54-235-247-209.compute-1.amazonaws.com:5432/d6pq4pd96n8bci'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=16)])
    email = StringField('Email', validators=[InputRequired(), Email(message='invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    custom_css = '<link rel="stylesheet" href="../static/main.css">'
    return render_template('landing.html', custom_css=custom_css)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return f'<p>{form.username.data} {form.password.data}</p>'
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        message = 'Account created successfully, please login!'
        return render_template('signup.html', form=form, message=message)
        # return f'<p>{form.username.data} {form.password.data} {form.email.data}</p>'
    return render_template('signup.html', form=form)
