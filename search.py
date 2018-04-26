from apiclient.discovery import build
from database import Base
from models import Song
from config import YOUTUBE_API_VERSION, YOUTUBE_API_SERVICE_NAME, DEVELOPER_KEY


def convert(search_result):
  song_id = search_result['id']['videoId']
  title = search_result['snippet']['title']
  thumbnail_url = search_result['snippet']['thumbnails']['default']['url']
  s = Song(youtube_hash=song_id, title=title, thumbnail_url=thumbnail_url)
  return s


def youtube_search(target_name):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=target_name,
    part="id,snippet",
    maxResults=15
  ).execute()

  response = search_response.get('items', [])
  videos = [convert(vid) for vid in response if vid['id']['kind'] =='youtube#video']
  return videos
