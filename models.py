from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.security import check_password_hash, generate_password_hash
from database import Base


class User(Base):

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

    playlists = relationship('Playlist', backref='users')

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
            'playlists': self.playlists
        }

    def __repr__(self):
        """
        Return str of class User.
        """
        return 'User name %s' % self.username


class Playlist(Base):
    """
    Class that contains information about Playlists.

    Attributes:
        id (:obj:`int`, unique): id of Playlist.
        name (:obj:`str`, not nullable): name of Playlist.
        user_id (:obj:`int`, ForeignKey): id of owner of Playlist.
        
    """

    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    songs = relationship('Song', backref='playlists')

    @property
    def serialize(self):
        """
        Return diction of class properties.
        """
        return {
            'name': self.name,
            'songs': self.songs
        }

    def __repr__(self):
        """
        Return str of class Playlist.
        """
        return '<Playlist name: %s>' % self.name


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
    name = Column(String(200), nullable=False)
    author = Column(String(200), nullable=False)

    playlist_ids = Column(Integer, ForeignKey('playlists.id'))

    @property
    def serialize(self):
        """
        Return diction of class properties.
        """
        return {
            'name': self.name,
            'author': self.author
        }

    def __repr__(self):
        """
        Return str of class Song.
        """
        return '<Song (id: %d, name: %s, author: %s)>' % (self.id, self.name, self.author)
