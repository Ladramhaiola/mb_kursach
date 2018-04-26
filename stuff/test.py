from requests import put, get, delete, post

url = 'http://localhost:8080/api/songs'
data = {"userid":1}

print(get(url, data=data).text)