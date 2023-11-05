from . import db
from flask_login import UserMixin
import sqlalchemy as sa
import enum
from sqlalchemy.sql import func

class UserType(enum.Enum):
    admin = 'admin'
    ordinary = 'ordinary'

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String(50), nullable=False)
    email = sa.Column('email', sa.String(150), nullable=False, unique=True)
    type = sa.Column('type', sa.Enum(UserType), nullable=False, default=UserType.ordinary)
    pwhash = sa.Column('pwhash', sa.String(200), nullable=False)
    records = db.relationship('Record')

class Record(db.Model):
    id = sa.Column('id', sa.Integer, primary_key=True)
    user_id = sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    emoji = sa.Column('emoji', sa.Integer, nullable=False)
    datetime = sa.Column('datetime', sa.DateTime, default=func.now())

