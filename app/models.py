from flask import url_for
from matplotlib.pyplot import title
from sqlalchemy.orm import backref,relationship
from sqlalchemy.exc import IntegrityError
from app import db, login
from flask_login import UserMixin
import json
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import base64
from datetime import datetime, timedelta
import os

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page,False)
        data = {
                'items': [item.to_dict() for item in resources.items],
                '_meta': {
                    'page': page,
                    'per_page': per_page,
                    'total_pages': resources.pages,
                    'total_items' : resources.total
                },
                '_links': {
                    'self': url_for(endpoint,page=page,per_page=per_page,**kwargs),
                    'next': url_for(endpoint,page=page + 1, per_page=per_page,**kwargs) if resources.has_next else None,
                    'prev': url_for(endpoint,page=page - 1, per_page=per_page,**kwargs) if resources.has_prev else None
                }
        }
        return data

class User(UserMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Project(PaginatedAPIMixin,db.Model):

    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),index=True,unique=True)
    summary = db.Column(db.String(255),index=True,unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)


    def __repr__(self):
        return '<Title {}>'.format(self.title)

    def to_dict(self):
        data = {
            'id':self.id,
            'title': self.title,
            'summary':self.summary,
            'user_id':self.user_id,
            'start_time':str(self.start_time),
            'end_time':str(self.end_time),
            '_links': {
                'self': url_for('api.get_project',title=self.title)
            }
        }
        return data

    def from_dict(self,data):
        for field in data:
            setattr(self,field,data[field])