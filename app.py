from flask import Flask, json, redirect, render_template, request, session, url_for
from database import db_session, init_db, delete_Playlist, add_Playlist, get_Playlists, add_Song, get_Songs
from models import User, Song, Playlist
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'total secret'


@app.route('/')
def index():
    return render_template('signin.html')


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
            session['user'] = {'username': username, 'logged_in': True}
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
                session['user'] = {'username': username, 'logged_in': True}
                return redirect(url_for('secret'))
            else:
                return 'wrong password'
        return 'Account does not exist'
    else:
        return render_template('signin.html')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('signin'))


@app.route('/secret')
def secret():
    u = session['user']
    return '<h1>%s</h1><a href="/logout">Log Out</a>' % str(u)


@app.teardown_appcontext
def shutdown_session(param):
    print(param)
    db_session.remove()


init_db()
 app.run('localhost', 8080, debug=True)
