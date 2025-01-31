from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, marshal, marshal_with, fields, abort
from flask_security import auth_required, hash_password, roles_required, current_user
from flask_security.datastore import SQLAlchemyUserDatastore
from sqlalchemy.exc import IntegrityError
from model import db, User as userdata ,Role, Song as songdata, Album as albumdata, Playlist as playlistdata, Rating as ratingdata
from cache import cache
from statistics import mean
from datetime import datetime

datastore=SQLAlchemyUserDatastore(db,userdata,Role)

api = Api(prefix = '/api')

#############################################################################################################
# Parser for parsing request data
user_parser = reqparse.RequestParser()
user_parser.add_argument('password', type=str, help='password of the user')
user_parser.add_argument('email', type=str, help='email of the user')
user_parser.add_argument('username', type=str, help='username of the user')
user_parser.add_argument('role', type=str, help='role of the user', required = True)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'flag' : fields.Boolean,
    'roles': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
    })),
}

class User(Resource):
    @auth_required('token')
    def get(self, email=None):
        if email:
            # If email is provided, fetch the user_id for that email
            user = userdata.query.filter_by(email=email).first()
            if user:
                role = user.roles[0].name if user.roles else None
                return {'user_id': user.id,'user_name': user.username, 'role': role, 'flag' : user.flag}
            else:
                return {'error': 'User not found'}, 404
        else:
            # If no email is provided, return all users
            all_users = userdata.query.all()

            formatted_users = [
                marshal(user, user_fields) for user in all_users
            ]

            return formatted_users
    
    # @marshal_with(user_fields)
    def post(self):
        args=user_parser.parse_args()
        email = args.get("email")
        user_name = args.get("username")
        passw = args.get("password")
        role_name = args.get("role","user")

        check=userdata.query.filter_by(email=email).first()
        if check:
           abort(409, description='Email you entered already belongs to an account. Try another email.')
        check=userdata.query.filter_by(username=user_name).first()
        if check:
           abort(409, description='Username you entered already belongs to an account. Try another username.')
        
        role = datastore.find_role(role_name)
        
        datastore.create_user(email=email, 
                              username=user_name, 
                              password=hash_password(passw), 
                              roles=[role])
        db.session.commit()
        return {'message': 'New user created Successfully'}
    

    @cache.memoize(timeout=10)
    @auth_required('token')
    def put(self, email):
        user = userdata.query.filter_by(email=email).first()
        if user:
            args = user_parser.parse_args()
            role_name = args.get("role")
            role = datastore.find_role(role_name)
            user.roles = [role]  # Update user's role
            db.session.commit()
            return {'message': f'Role status updated successfully for {user.email}'}
        else:
            return {'error': 'User not found'}, 404

    @auth_required('token')
    @roles_required('admin')
    def delete(self, id):
        # if email != "admin@gmail.com":
        #     return {'error': 'Permission denied. Only admin@gmail.com can delete users.'}, 403

        user = userdata.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': f'User {user.id} deleted successfully'}
        else:
            return {'error': 'User not found'}, 404
    
api.add_resource(User,'/user','/user/<string:email>','/user/<int:id>','/user/<int:id>')



####################################################################
# Define request parser
song_parser = reqparse.RequestParser()
song_parser.add_argument('title', type=str, help='Title of the song')
song_parser.add_argument('artist', type=str, help='Artist of the song')
song_parser.add_argument('lyrics', type=str, help='lyrics of the song')
song_parser.add_argument('genre', type=str, help='genre of the song')
song_parser.add_argument('user_id', type=int, help=' user_id of the album')
song_parser.add_argument('album_id', type=int, help='album_id of the song')

# Define resource fields
song_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'artist': fields.String,
    'lyrics': fields.String,
    'genre': fields.String,
    'releasedate': fields.DateTime(dt_format='iso8601'),
    'user_id': fields.String,
    'album_id': fields.Integer,
    'flag' : fields.Boolean
}

# Resources
class Song(Resource):
    @auth_required('token')
    def get(self, song_id=None):
        if song_id is None:
            songs = songdata.query.order_by(songdata.releasedate.desc()).all()
            # Populate count of ratings for each song
            songs_display = []
            for song in songs:
                song_data = {
                    'id': song.id,
                    'title': song.title,
                    'artist': song.artist,
                    'genre': song.genre,
                    'releasedate': song.releasedate,
                    'user_id': song.user_id,
                    'album_id': song.album_id,
                    'flag': song.flag,
                }
                songs_display.append(song_data)
            return jsonify(songs_display)
        
        else:
            user_id = current_user.id
            rating = ratingdata.query.filter_by(song_id=song_id, user_id=user_id).first()
            song = songdata.query.get(song_id)
            if song:
                song_data = {
                    'id': song.id,
                    'title': song.title,
                    'artist': song.artist,
                    'lyrics': song.lyrics,
                    'genre': song.genre,
                    'flag': song.flag,
                    'releasedate': song.releasedate,
                    'user_id': song.user_id,
                    'album_id': song.album_id,
                    'rating_count': get_rating_count(song.id),
                    'hasRated': rating is not None,
                    'rating': rating.rating if rating is not None else "0",
                    'album_title': song.album.title if song.album else "No Album"
                }
                return jsonify(song_data)
            else:
                return {'message': 'Song not found'}, 404

    @auth_required('token')
    @roles_required('creator')
    def post(self):
        args = song_parser.parse_args()
        
        # Check if a song with the same title exists
        existing_song = songdata.query.filter_by(title=args['title']).first()
        if existing_song:
            return {'message': 'A song with the same title already exists'}, 400
        
        # Check if a song with the same lyrics exists
        existing_lyrics = songdata.query.filter_by(lyrics=args['lyrics']).first()
        if existing_lyrics:
            return {'message': 'A song with the same lyrics already exists'}, 400
        
        song = songdata(title=args['title'], artist=args['artist'], 
                    lyrics=args['lyrics'], genre=args['genre'], 
                    user_id=args['user_id'], album_id=args['album_id'], releasedate = datetime.utcnow())
        
        try:
            db.session.add(song)
            db.session.commit()
            formatted_song = marshal(song, song_fields)
            return formatted_song, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Error occurred while adding the song to the database'}, 500

   
    # @roles_required('admin' , 'creator')
    @auth_required('token')
    def delete(self, song_id):
        print(f"Current user ID: {current_user.id}, Roles: {current_user.roles}")
        song = songdata.query.get(song_id)
        # Check if the current user is authorized to delete the album
        if not song:
            return {'message': 'Song not found'}, 404
        if song and ((song.user_id == current_user.id) or (current_user.id == 1 )):  
            db.session.delete(song)
            db.session.commit()
            return '', 204
        else:
            abort(403, message="You are not authorized to delete this song")

    @auth_required('token')
    @roles_required('creator')
    def put(self, song_id):
        args = song_parser.parse_args()
        song = songdata.query.get(song_id)
        
        if not song:
            return {'message': 'Song not found'}, 404
        
        if song.user_id != current_user.id:
            abort(403, message="You are not authorized to delete this album")
        
        # Check if the updated title already exists
        if args['title'] != song.title and songdata.query.filter_by(title=args['title']).first():
            return {'message': 'Title already exists'}, 400
        
        # Check if the updated lyrics already exist
        if args['lyrics'] != song.lyrics and songdata.query.filter_by(lyrics=args['lyrics']).first():
            return {'message': 'Lyrics already exist for another song'}, 400

        # Update all fields
        song.title = args['title'] if args['title'] else song.title
        song.artist = args['artist'] if args['artist'] else song.artist
        song.lyrics = args['lyrics'] if args['lyrics'] else song.lyrics
        song.genre = args['genre'] if args['genre'] else song.genre
        song.album_id = args['album_id'] if args['album_id'] else song.album_id

        try:
            db.session.commit()
            formatted_song = marshal(song, song_fields)
            return formatted_song, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Integrity Error'}, 500
# Define routes
api.add_resource(Song, '/songs', '/songs/<int:song_id>')

def get_rating_count(song):
    # Fetch all ratings for the given song
    ratings = [rating.rating for rating in ratingdata.query.filter_by(song_id=song).all()]
    
    # Check if the ratings list is not empty
    if ratings:
        # Calculate the mean if there are ratings
        return mean(ratings)
    else:
        # Return a default value if there are no ratings
        return None


########################################################################### 

# Define request parser for albums
album_parser = reqparse.RequestParser()
album_parser.add_argument('title', type=str, help='Title of the album')
album_parser.add_argument('description', type=str, help='Description of the album')
album_parser.add_argument('user_id', type=str, help='User_id of the album')
album_parser.add_argument('assign_songs', type=int, action='append', help='IDs of songs to assign to the album')
album_parser.add_argument('remove_songs', type=int, action='append', help='IDs of songs to remove from the album')

# Define resource fields for albums
album_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    "user_id": fields.Integer,
}

# Resources for albums
class Album(Resource):
    @auth_required('token')
    def get(self, album_id=None):
        if album_id is None:
            all_albums = albumdata.query.order_by(albumdata.id.desc()).all()
            formatted_albums = [
                marshal(album, album_fields) for album in all_albums
            ]
            return formatted_albums
        
        album = albumdata.query.get(album_id)
        if not album:
            return {'message': 'Album not found'}, 404
        
        # If album ID is provided, fetch associated songs
        songs = album.song.all()  # Assuming 'song' is the relationship in the Album model
        formatted_album = marshal(album, album_fields)
        formatted_album['songs'] = [
            marshal(song, song_fields) for song in songs
        ]
        return formatted_album

    # @marshal_with(album_fields)
    @auth_required('token')
    @roles_required('creator')
    def post(self):
        args = album_parser.parse_args()
        title = args['title']
        description = args['description']
        user_id = args['user_id']
        
        check=albumdata.query.filter_by(title=title).first()
        if check:
           abort(400, message= 'title you entered already available. Try another title.')
        # Create the album
        album = albumdata(title=title, description=description, user_id=user_id)
        db.session.add(album)
        db.session.commit()
        
        # # Associate songs with the album
        # if songs != None:
        #     for song_id in songs:
        #         song = songdata.query.filter_by(id=song_id).first()
        #         # Check if the song is already associated with any other album
        #         existing_album = albumdata.query.filter(albumdata.song.any(id=song_id)).first()
        #         if existing_album:
        #             abort(400 , message = f'The song with ID {song_id} is already associated with the album "{existing_album.title}".')
        #         if song:
        #             album.song.append(song)
        #         db.session.commit()
        
        # Marshal the album object before returning
        formatted_album = marshal(album, album_fields)
        return formatted_album, 201
    
    @auth_required('token')
    def delete(self, album_id):
        album = albumdata.query.get(album_id)
        if not album:
            return {'message': 'Album not found'}, 404
        # print(album.user_id)
        # Check if the current user is authorized to delete the album
        if album.user_id == current_user.id or current_user.id == 1 :
            db.session.delete(album)
            db.session.commit()
            return '', 204
        else:
            abort(403, message="You are not authorized to delete this album")

    # @marshal_with(album_fields)
    @auth_required('token')
    @roles_required('creator')
    def put(self, album_id):
        args = album_parser.parse_args()
        album = albumdata.query.get(album_id)
        if not album:
            return {'message': 'Album not found'}, 404
        # Check if the current user is authorized to delete the album
        if album.user_id != current_user.id:
            abort(403, message="You are not authorized to update this album")
        
        # Update album details
        album.title = args['title']
        album.description = args['description']
        db.session.commit()
        
        # Assign songs to the album
        if args['assign_songs']:
            for song_id in args['assign_songs']:
                 # Check if the song is already associated with any other album
                existing_album = albumdata.query.filter(albumdata.song.any(id=song_id)).first()
                if existing_album:
                    return jsonify({'error': f'The song with ID {song_id} is already associated with the album "{existing_album.title}".'}), 400
                song = songdata.query.get(song_id)
                if song:
                    album.song.append(song)
                    db.session.commit()
                else:
                    return {'message': f'Song with ID {song_id} not found'}, 404
        
        # Remove songs from the album
        if args['remove_songs']:
            for song_id in args['remove_songs']:
                song = songdata.query.get(song_id)
                try: 
                    if song in album.song:
                        album.song.remove(song)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return f"Error deleting song: {str(e)}", 500
        # Marshal the album object before returning
        formatted_album = marshal(album, album_fields)
        return formatted_album, 201

# Define routes for albums
api.add_resource(Album, '/albums', '/albums/<int:album_id>')


#################################################################################################

# Define request parser for playlists
playlist_parser = reqparse.RequestParser()
playlist_parser.add_argument('title', type=str, help='Title of the playlist')
playlist_parser.add_argument('user_id', type=int, help='Title of the playlist')
playlist_parser.add_argument('songs',  type=int, action='append', location = "json", help='List of song IDs in the playlist')

playlist_fields = {
    'id': fields.Integer,
    'title' : fields.String
}

# Resources for playlists
class Playlist(Resource):
    #@marshal_with(playlist_fields)
    @auth_required('token')
    def get(self, playlist_id=None):
        if playlist_id is None:
            all_playlist = playlistdata.query.order_by(playlistdata.id.desc()).filter(playlistdata.user_id == current_user.id).all()
            formatted_playlists = [
                marshal(playlist, playlist_fields) for playlist in all_playlist
            ]
            return formatted_playlists
        
        playlist = playlistdata.query.get(playlist_id)
        if not playlist:
            return {'message': 'Playlist not found'}, 404
        
        songs = playlist.songs.all()
        formatted_playlist = marshal(playlist, playlist_fields)
        formatted_playlist['songs'] = [
             {
                    'id': song.id,
                    'title': song.title,
                    'artist': song.artist,
                    'genre': song.genre,
                    'user_id': song.user_id,
                    'album_id': song.album_id,
                    'rating_count': get_rating_count(song.id)
                } for song in songs
        ]
        return formatted_playlist
    

    #@marshal_with(playlist_fields)
    @auth_required('token')
    def post(self):
        args = playlist_parser.parse_args()
        if playlistdata.query.filter_by(user_id=args['user_id'], title=args['title']).first():
            abort(400, message='Title you entered is already in use. Try another title.')
        
        new_playlist = playlistdata(title=args['title'], user_id=args['user_id'])
        if args['songs']:
            song_ids = set(args['songs'])  # Removing duplicates
            songs = songdata.query.filter(songdata.id.in_(song_ids)).all()
            if len(songs) != len(song_ids):
                abort(400, message="One or more song IDs are invalid.")
            new_playlist.songs.extend(songs)
        
        db.session.add(new_playlist)
        db.session.commit()
        
        return jsonify({"message": "Playlist created successfully", "playlist_id": new_playlist.id})
    
    def delete(self, playlist_id):
        playlist = playlistdata.query.get(playlist_id)
        if not playlist:
            return {'message': 'Playlist not found'}, 400
        
        # Check if the current user is authorized to delete the album
        if playlist.user_id == current_user.id or current_user.id == 1 :
            db.session.delete(playlist)
            db.session.commit()
            return '', 204
        else:
            abort(403, message="You are not authorized to delete this album")

    #@marshal_with(playlist_fields)
    @auth_required('token')
    def put(self, playlist_id):
        args = playlist_parser.parse_args()
        playlist = playlistdata.query.get(playlist_id)
        if not playlist:
            return {'message': 'Playlist not found'}, 404

        if playlist.user_id != current_user.id:
            abort(403, message="You are not authorized to update this playlist")

        if args['songs']:
            current_songs = set(s.id for s in playlist.songs)
            for song_id in args['songs']:
                if song_id in current_songs:
                    continue  # Skip this song as it is already in the playlist
                song = songdata.query.get(song_id)
                if not song:
                    return {'message': f'Song with ID {song_id} not found'}, 404
                playlist.songs.append(song)
            
            try:
                db.session.commit()
                return {'message': 'Songs successfully added to the playlist'}, 200
            except Exception as e:
                db.session.rollback()
                return {'message': 'Error occurred while updating the playlist: {}'.format(e)}, 500

        return {'message': 'No songs provided'}, 400


# Define routes for playlists
api.add_resource(Playlist, '/playlists', '/playlists/<int:playlist_id>')




###########################################################################################################
# Define request parser for song ratings
# Update rating_parser to accept rating values from 1 to 5, user_id, and song_id
rating_parser = reqparse.RequestParser()
rating_parser.add_argument('rating', type=int, required=True, help='Rating must be an integer between 1 and 5', choices=[1, 2, 3, 4, 5])
rating_parser.add_argument('user_id', type=int, required=True, help='User ID must be provided')
rating_parser.add_argument('song_id', type=int, required=True, help='Song ID must be provided')

# Define rating_fields for marshalling
rating_fields = {
    'id': fields.Integer,
    'rating': fields.Integer,
    'user_id': fields.Integer,
    'song_id': fields.Integer
}

# Resources for song ratings
class SongRating(Resource):
    @marshal_with(rating_fields)
    def get(self, rating_id=None):
        if not rating_id:
            ratings = ratingdata.query.all()
            return ratings  # This will use the defined fields to marshal the list of ratings
        rating = ratingdata.query.get(rating_id)
        if not rating:
            abort(404, message='Rating not found')
        return rating

    @marshal_with(rating_fields)
    def post(self):
        args = rating_parser.parse_args()
        # Check if the user has already rated the song
        existing_rating = ratingdata.query.filter_by(user_id=args['user_id'], song_id=args['song_id']).first()
        if existing_rating:
            abort(400, message='User has already rated this song')
        
        # Create and add new rating
        new_rating = ratingdata(rating=args['rating'], user_id=args['user_id'], song_id=args['song_id'])
        db.session.add(new_rating)
        db.session.commit()

        # After saving, return the new rating using marshalling
        return new_rating, 201  # This uses marshal_with to format the response

# Define routes for song ratings
api.add_resource(SongRating, '/ratings', '/ratings/<int:rating_id>')

from task import exportjob

class Export(Resource):
    def get(self, email = None):
        data =[]
        albums = albumdata.query.all()
        for album in albums:
            album_dict = {'Album_Title' : album.title, 'Album_Description' : album.description, 'Album_User': album.user.username, 'Album_Songs' : []}
            for song in album.song :
                song_dict = {'Song_Title' : song.title, 'Song_Artist' : song.artist, 'Song_Genere' : song.genre, 'Song_Releasedate' : song.releasedate}
                album_dict['Album_Songs'].append(song_dict)
            data.append(album_dict)
        exportjob.delay(data, email, username = "Admin")
        
        return jsonify({'Message' : 'Export Done!'})
    
api.add_resource(Export, '/export/<string:email>')

##############################################################################################################

class FlagSong(Resource):
    @auth_required('token')
    def put(self, song_id):
        song = songdata.query.get(song_id)
        if not song:
            abort(404, message="Song not found")
        
        song.flag = not song.flag  # Toggle the current flag status
        db.session.commit()
        return {'message': f"Flag status updated for song with ID {song_id}: {song.flag}"}

api.add_resource(FlagSong, '/flag-song/<int:song_id>')


###############################################################################################################3

class FlagUser(Resource):
    @auth_required('token')
    @roles_required('admin')
    def put(self, user_id):
        user = userdata.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        
        user.flag = not user.flag  # Toggle the current flag status
        db.session.commit()
        return {'message': f"Flag status updated for user with ID {user_id}: {user.flag}"}

api.add_resource(FlagUser, '/flag-user/<int:user_id>')