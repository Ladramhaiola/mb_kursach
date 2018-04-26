from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_restful import reqparse, abort, Resource, fields, marshal_with

engine = create_engine(
    'mysql+pymysql://kursach:Wb7Q4_Yo?86q@den1.mysql1.gear.host:3306/kursach')
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db_session.commit()


from models import User, Song, Association

song_fields = {
    'title': fields.String,
    'youtube_hash': fields.String,
    'thumbnail_url': fields.String
}

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('youtube_hash', type=str)
parser.add_argument('thumbnail_url', type=str)
parser.add_argument('userid', type = int)

def find_association(user_id: int, s: Song):
    return db_session.query(Association).filter(Association.user_id == user_id).filter(Association.song_id == s.id).first()

class SongResource(Resource):

    @marshal_with(song_fields)
    def get(self):
        args = parser.parse_args()
        youtube_hash = args['youtube_hash']
        s = db_session.query(Song).filter(Song.youtube_hash == youtube_hash).first()
        if not s:
            abort(404, message='Song {} not found'.format(youtube_hash))
        return s

    @marshal_with(song_fields)
    def put(self):
        args = parser.parse_args()
        user_id = args["userid"]
        youtube_hash = args['youtube_hash']
        s = db_session.query(Song).filter(Song.youtube_hash == youtube_hash).first()
        if not s: 
            title = args['title']
            thumbnail_url = args['thumbnail_url']
            s = Song(youtube_hash=youtube_hash, title=title, thumbnail_url=thumbnail_url)
            db_session.add(s)
            db_session.commit()
        if find_association(user_id, s):    
            a = Association(user_id = user_id, song_id = s.id)
            db_session.add(a)
            db_session.commit()
        return s, 201

    def delete(self):
        args = parser.parse_args()
        user_id = args["userid"]
        youtube_hash = args['youtube_hash']
        s = db_session.query(Song).filter(Song.youtube_hash == youtube_hash).first()
        if not s:
            abort(404, message="Todo {} doesn't exist".format(id))
        a = find_association(user_id,s)
        if a:
            db_session.delete()
            db_session.commit()
        return {}, 204


class SongListResource(Resource):
    @marshal_with(song_fields)
    def get(self):
        args = parser.parse_args()
        user_id = args["userid"]
        a = db_session.query(Association).filter(Association.user_id == user_id).all()
        s = [db_session.query(Song).filter(Song.id == i.song_id).first() for i in a]
        return s