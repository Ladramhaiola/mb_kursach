from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from models import User, Playlist, Song

engine = create_engine('mysql+pymysql://kursach:Lv1q9veCY-_f@den1.mysql2.gear.host:3306/kursach')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

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
	

	pass