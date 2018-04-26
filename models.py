from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash
from database import Base
from flask_login import UserMixin
from flask_restful import reqparse, Resource, Api

class Association(Base):
    __tablename__ = 'association'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True)
    song = relationship("Song", back_populates="users")
    user = relationship("User", back_populates="songs")

class User(Base, UserMixin):

    """
    Class that contains information about Users.
    Attributes:
        id (:obj:`int`, unique): id of User.
        username (:obj:`str`, unique, not nullable): username of User.
        password (:obj:`str`, not nullable): password of User.
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    songs = relationship('Association', back_populates="user")

    def __init__(self, username, password):
        """
        Args:
            sername (:obj:`str`, unique, not nullable): username of User.
            password (:obj:`str`, not nullable): password of User.
        """
        self.username = username
        self.password = generate_password_hash(password)

    @property
    def serialize(self):
        """
        Return diction of class properties.
        """
        return {
            'username': self.username,
            'songs': self.songs
        }

    def __repr__(self):
        """
        Return str of class User.
        """
        return 'User name %s' % self.username


class Song(Base):
    """
    Class that contains information about Songs.
    Attributes:
        id (:obj:`int`, unique): id of Song.
        name (:obj:`str`, not nullable): name of Song.
        author (:obj:`str`, not nullable): name of Song.
        user_id (:obj:`int`, ForeignKey): id of owner of Playlist.
        
    """
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    youtube_hash = Column(String(200))
    title = Column(String(200), nullable=False)
    thumbnail_url = Column(String(200))

    users = relationship(
        "Association",
        back_populates="song")

    @property
    def serialize(self):
        """
        Return diction of class properties.
        """
        return {
            'youtube_hash': self.youtube_hash,
            'title': self.title,
            'thumbnail_url': self.thumbnail_url
        }

    def __repr__(self):
        """
        Return str of class Song.
        """
        return '<Song (title: %s, url: %s)>' % (self.title, self.thumbnail_url)