from .database import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='User', passive_deletes=True)

class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, unique=True, nullable=False)
    filename = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('User.id', ondelete="CASCADE"), nullable=False)

class Follow(db.Model):
    __tablename__ = 'Follow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user_name = db.Column(db.String, nullable=False)
    follows_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    follows_name = db.Column(db.String, nullable=False)
    date_followed = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.relationship("User", foreign_keys=[user_id])
    follows = db.relationship("User", foreign_keys=[follows_id])