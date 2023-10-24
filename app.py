from flask import Flask, send_from_directory, redirect, request
from detect import *
import json

albums = get_albums()

app = Flask(__name__)

def success(data):
    return json.dumps({'success': True, 'data': data}), 200, {'ContentType': 'application/json' }

def error(message):
    return json.dumps({'success': False, 'error': message}), 400, {'ContentType': 'application/json' }


# API

@app.route('/api/albums')
def get_albums():
    return success([album_name for album_name in albums])

@app.route('/api/albums/<album_name>')
def get_album(album_name):
    album = albums[album_name]
    if album is None:
        return success(None)
    return success(album.to_dict())

@app.route('/api/albums/<album_name>/search')
def get_album_search(album_name):
    album = albums[album_name]
    if album is None:
        return error('album not found')
    if request.args.get('pictureIndex') != None and request.args.get('faceIndex') != None:
        pictureIndex = int(request.args.get('pictureIndex'))
        if 0 > pictureIndex or pictureIndex >= len(album.pictures):
            return error('picture not found')
        picture = album.pictures[pictureIndex]
        faceIndex = int(request.args.get('faceIndex'))
        if 0 > faceIndex or faceIndex >= len(picture.encodings):
            return error('face not found')
        encoding = picture.encodings[faceIndex]
        return success(album.get_search_by_face(encoding))
    elif request.args.get('picture'):
        pic = Picture.from_base64(request.args.get('picture'))
        if len(pic.encodings) == 0:
            return error('no face found')
        return success(album.get_search_by_face(pic.encodings[0]))
    else:
        return error('missing parameters')


# Photos

@app.route('/photos/<path:path>')
def get_photo(path):
    return send_from_directory('photos', path)


# Front

@app.route('/<path:path>')
def get_front(path):
    return send_from_directory('front/dist', path)

@app.route('/')
def get_index():
    return send_from_directory('front/dist', 'index.html')