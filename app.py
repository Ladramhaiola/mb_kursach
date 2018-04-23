from flask import Flask, json, redirect, render_template, request, session, url_for, jsonify
from database import db_session, init_db, delete_Playlist, add_Playlist, get_Playlists, add_Song, get_Songs
from models import User
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'total secret'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('signin.html')

@app.route('/main')
def index1():
    return render_template('main.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        s = db_session.query(User).filter(User.username == username).first()
        if not s:
            u = User(username=username, password=password)
            db_session.add(u)
            db_session.commit()
            login_user(u)
            return redirect(url_for('secret'))
        return 'Account already exists'
    else:
        return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        s = db_session.query(User).filter(User.username == username).first()
        if s:
            if check_password_hash(s.password, password):
                login_user(s)
                return redirect(url_for('secret'))
            else:
                return 'wrong password'
        return 'Account does not exist'
    else:
        return render_template('signin.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('signin'))


@app.route('/secret')
@login_required
def secret():
    return '<h1>%s</h1><a href="/logout">Log Out</a>' % current_user.username

@app.teardown_appcontext
def shutdown_session(param):
    db_session.remove()


init_db()
app.run('localhost', 8080, debug=True)
