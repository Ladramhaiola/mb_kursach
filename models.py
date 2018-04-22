from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.security import check_password_hash, generate_password_hash
from database import Base

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String(200), unique=True, nullable=False)
	password = Column(String(200), nullable=False)

	playlists = relationship('Playlist', backref='users')

	def __init__(self, username, password):
		self.username = username
		self.password = generate_password_hash(password)

	@property
	def serialize(self):
		return {
			'username': self.username,
			'playlists': self.playlists
		}

	def __repr__(self):
		return 'User name %s' % self.username

class Playlist(Base):
	__tablename__ = 'playlists'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(200), nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'))

	songs = relationship('Song', backref='playlists')

	@property
	def serialize(self):
		return {
			'name': self.name,
			'songs': self.songs
		}

	def __repr__(self):
		return '<Playlist name: %s>' % self.name

class Song(Base):
	__tablename__ = 'songs'
	id = Column(Integer, primary_key=True)
	name = Column(String(200), nullable=False)
	author = Column(String(200), nullable=False)

	playlist_ids = Column(Integer, ForeignKey('playlists.id'))

	@property
	def serialize(self):
		return {
			'name': self.name,
			'author': self.author
		}

	def __repr__(self):
		return '<Song (id: %d, name: %s, author: %s)>' % (self.id, self.name, self.author)
