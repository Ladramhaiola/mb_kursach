from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    'mysql+pymysql://kursach:Lv1q9veCY-_f@den1.mysql2.gear.host:3306/kursach')
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

from models import User, Playlist, Song


def init_db():

    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db_session.commit()


def add_Playlist(username, playlistname):
    p = Playlist(name=playlistname)
    db_session.add(p)
    u = db_session.query(User).filter(User.username == username).first()
    u.playlists.append(p)
    db_session.commit()


def get_Playlists(username):
    u = db_session.query(User).filter(User.username == username).first()
    return u.playlists


def delete_Playlist(username, playlistname):
    u = db_session.query(User).filter(User.username == username).first()
    p = db_session.query(Playlist).filter(
        Playlist.name == playlistname and Playlist.user_id == u.id).first()
    db_session.delete(p)
    db_session.commit()


def add_Song(username, name, author, playlistname):
    u = db_session.query(User).filter(User.username == username).first()
    p = db_session.query(Playlist).filter(
        Playlist.name == playlistname and Playlist.user_id == u.id).first()
    s = Song(name=name, author=author)
    db_session.add(s)
    p.songs.append(s)
    db_session.commit()


def get_Songs(username, playlistname):
    u = db_session.query(User).filter(User.username == username).first()
    p = db_session.query(Playlist).filter(
        Playlist.name == playlistname and Playlist.user_id == u.id).first()
    return p.songs


def delete_Song(username, playlistname):
    u = db_session.query(User).filter(User.username == username).first()
    p = db_session.query(Playlist).filter(
        Playlist.name == playlistname and Playlist.user_id == u.id).first()
    db_session.delete(p)
    db_session.commit()
