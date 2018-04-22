from flask import Flask, json, redirect, render_template, request, session
from models import User, Song, Playlist
from database import db_session, init_db
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key =  'total secret'

@app.route('/')
def index():
	return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	username = request.form['username']
	password = request.form['password']
	s = db_session.query(User).filter(User.username == username).first()
	if not s:
		u = User(username=username, password=password)
		db_session.add(u)
		db_session.commit()
		session['user'] = {'username':username, 'logged_in': True}
		return 'Success'
	return 'Accoun already exists'

@app.teardown_appcontext
def shutdown_session(param):
	print(param)
	db_session.remove()

init_db()
app.run('localhost', 8080, debug=True)