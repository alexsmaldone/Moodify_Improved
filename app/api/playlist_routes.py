from flask import Blueprint, abort, request
from app.models import Playlist, Library, db
from app.forms.new_playlist_form import NewPlaylistForm

playlist_routes = Blueprint('playlists', __name__)


def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{error}')
    return errorMessages



@playlist_routes.route('/<int:id>')
def playlist(id):
    playlist = Playlist.query.get(id)

    if playlist is None:
        abort(404)

    playlist_songs = playlist.library
    playlist_songs_dicts = [song.to_dict() for song in playlist_songs]
    return playlist.to_dict()


@playlist_routes.route('/')
def playlists():
    playlists = Playlist.query.all()
    playlists_dicts = [playlist.to_dict() for playlist in playlists]

    return { "playlists": playlists_dicts }

@playlist_routes.route('/', methods=["POST"])
def post_playlist():
    form = NewPlaylistForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        playlist = Playlist(name=form.data['name'], mood_id=form.data['mood_id'], user_id=form.data['user_id'])

        db.session.add(playlist)

        db.session.commit()

        return playlist.to_dict()
    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}

@playlist_routes.route('/<int:id>', methods=["PUT"])
def edit_playlist(id):
    form = NewPlaylistForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    playlist = Playlist.query.get(id)

    if form.validate_on_submit():
        playlist.name = form.data['name']
        playlist.mood_id = form.data['mood_id']
        playlist.user_id = form.data['user_id']
        db.session.add(playlist)
        db.session.commit()

        return playlist.to_dict()
    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}

@playlist_routes.route('/addSongsToPlaylist', methods=['GET', 'POST'])
def add_song_to_playlist():

    songId = request.json['songId']
    playlistId = request.json['playlistId']


    song_new = Library.query.get(songId)
    playlist_new = Playlist.query.get(playlistId)


    song_new.playlists.append(playlist_new)
    db.session.commit()

    playlist = Playlist.query.get(playlistId)
    return playlist.to_dict()

@playlist_routes.route('/deleteSongFromPlaylist', methods=['DELETE'])
def delete_song_from_playlist():
    songId = request.json['songId']
    playlistId = request.json['playlistId']

    song = Library.query.get(songId)
    playlist = Playlist.query.get(playlistId)

    song.playlists.remove(playlist)
    db.session.commit()

    playlist = Playlist.query.get(playlistId)
    return playlist.to_dict()

@playlist_routes.route('/<int:id>', methods=["DELETE"])
def delete_playlist(id):
    playlist = Playlist.query.get(id)

    db.session.delete(playlist)
    db.session.commit()

    return {id: playlist.id}
