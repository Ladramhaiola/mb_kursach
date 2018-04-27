from requests import put, get, post, delete

url = 'http://localhost:8080/api/songs'
data = {"youtube_hash": "WzQBAc8i73E", "userid": 1,
        "title": "rabotai sobaka", "thumbnail_url": "urlll"}

resp = get(url, data=data)
print(resp.text)