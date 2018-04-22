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
	
	db_session.commit()