from flask import Flask, redirect, render_template, request, url_for, json, Response, jsonify, send_from_directory, session
from database import db_session, init_db, SongResource, SongListResource
from models import User, Song
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from search import youtube_search
from os import system, getcwd
from flask_restful import Api
import logging

app = Flask(__name__, static_folder='./static')
app.secret_key = 'total secret'

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

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
        app.logger.info('(signup) incoming data -> username: {0}, password: {1}'.format(username, password))
        s = db_session.query(User).filter(User.username == username).first()
        if not s:
            u = User(username=username, password=password)
            db_session.add(u)
            db_session.commit()
            login_user(u)
            app.logger.info('(signup) created new user -> {}'.format(str(u)))
            return redirect(url_for('secret'))
        app.logger.error('Account already exists')
        return 'Account already exists'
    else:
        return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app.logger.info('(signin) incoming data -> username: {0}, password: {1}'.format(username, password))
        s = db_session.query(User).filter(User.username == username).first()
        if s:
            if check_password_hash(s.password, password):
                login_user(s)
                app.logger.info('(signin) logged as user -> {}'.format(str(s)))
                return redirect(url_for('secret'))
            else:
                app.logger.error('(signin) wrong password for {}'.format(str(s)))
                return 'wrong password'
            app.logger('(signin) account {} does not exist'.format(str(s)))
        return 'Account does not exist'
    else:
        return render_template('signin.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('signin'))


@app.route('/secret', methods=['GET','POST', 'PUT'])
@login_required
def secret():
    return render_template('main.html')


@app.route('/api/search/<target>', methods=['PUT', 'GET', 'POST'])
@login_required
def look(target):
    resp = [vid.serialize for vid in youtube_search(target)]
    return jsonify({'user_id':current_user.id, 'result':resp})


api.add_resource(SongResource, '/api/song')
api.add_resource(SongListResource, '/api/songs')


@app.teardown_appcontext
def shutdown_session(param):
    db_session.remove()


@app.route('/api/serve/<youtube_hash>')
@login_required
def serve(youtube_hash):
    return send_from_directory('src', '{}.mp3'.format(youtube_hash))


init_db()
app.run('localhost', 8080, debug=True)