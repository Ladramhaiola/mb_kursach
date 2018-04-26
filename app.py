from flask import Flask, redirect, render_template, request, url_for, json, Response, jsonify, send_from_directory, session
from database import db_session, init_db, SongResource, SongListResource
from models import User, Song
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from search import youtube_search
from os import system, getcwd
from flask_restful import Api


app = Flask(__name__, static_folder='./static')
app.secret_key = 'total secret'

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
def logout():
    logout_user()
    return redirect(url_for('signin'))


@app.route('/secret')
def secret():
    return render_template('main.html')


@app.route('/api/search/<target>')
def look(target):
    resp = [vid.serialize for vid in youtube_search(target)]
    return jsonify(result = resp)


api.add_resource(SongResource, '/api/song')
api.add_resource(SongListResource, '/api/songs')


@app.teardown_appcontext
def shutdown_session(param):
    db_session.remove()
    

@app.route('/api/serve/<youtube_hash>')
def serve(youtube_hash):
    return send_from_directory('src', '{}.mp3'.format(youtube_hash))

init_db()
app.run('localhost', 8080, debug=True)