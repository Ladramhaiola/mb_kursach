from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mysql+pymysql://kursach:Lv1q9veCY-_f@den1.mysql2.gear.host:3306/kursach')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	from models import User, Playlist, Song
	# Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)

	# u1 = User(username='Sashenka :)', password='1234')
	# p1 = Playlist(name='aaiiii')
	# db_session.add(p1)
	# s1 = Song(name='I Hate everything about you', author='Three days grace')
	# db_session.add(s1)
	# p1.songs.append(s1)
	# u1.playlists.append(p1)
	# db_session.add(u1)

	db_session.commit()