from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()

# Association table for the many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)
# Association table for the many-to-many relationship between Playlists and Songs
playlist_song_link = db.Table(
    'playlist_songs',
    db.Column("playlist_id", db.Integer, db.ForeignKey('playlist.id'), primary_key = True),
    db.Column("song_id", db.Integer, db.ForeignKey('song.id'), primary_key = True)
)
# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    flag= db.Column(db.Boolean(), default=False, nullable = False)
    fs_uniquifier = db.Column(db.String(512), unique=True, nullable = False) # For Foursquare OAuth
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    playlists = db.relationship('Playlist', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    ratings = db.relationship('Rating', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    song = db.relationship('Song', backref = 'user')
    albums = db.relationship('Album', backref='user')

       
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(1000))
    

# Define Album model
class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    # flag= db.Column(db.Boolean(), default=False)
    song = db.relationship('Song', backref='album',  lazy='dynamic', cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    
# Define Song model
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    lyrics = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(), nullable=False)
    releasedate =db.Column(db.DateTime, default=datetime.now)
    flag= db.Column(db.Boolean(), default=False)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    rating =db.relationship('Rating', cascade= 'all, delete-orphan', backref = 'song')
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=True)

# Define Playlist model
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Song', secondary = 'playlist_songs', backref='playlists', lazy="dynamic")
    
# Define Rating model
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)

