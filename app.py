from flask import Flask

from database import db_session, init_db

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello'

@app.teardown_appcontext
def shutdown_session():
	db_session.remove()

init_db()
app.run('localhost', 8080, debug=True)