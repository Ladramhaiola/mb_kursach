from flask import Flask, json, redirect, render_template, request
from models import User, Song, Playlist
from database import db_session, init_db
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import Form, PasswordField, TextField, validators

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello'

@app.route('/search')
def search():
	res = User.query.filter(User.username == 'Sashenka').all()
	return '<p>%s</p>' % res

@app.route('/add')
def add():
	u = User(username='Alesha', password='1234intellect')
	db_session.add(u)
	try:
		db_session.commit()
	except IntegrityError:
		return 'duplicate'
	return json.dumps(u.serialize)

@app.teardown_appcontext
def shutdown_session(param):
	print(param)
	db_session.remove()

init_db()
app.run('localhost', 8080, debug=True)