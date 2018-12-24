import os
from flask import Flask, session, render_template
from flask_session import Session
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
from forms import LoginForm, RegisterForm

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'gs33sg34!pinndgSD45%lObN'
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


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
        return f'<p>{form.username.data} {form.password.data} {form.email.data}</p>'
    return render_template('signup.html', form=form)
