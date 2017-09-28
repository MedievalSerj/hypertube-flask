import os
import datetime
from flask import url_for, current_app
from flask_mail import Message
from werkzeug.security import generate_password_hash
from PIL import Image
from io import BytesIO
import base64
import uuid
from app import db, mail
from ..exceptions import ValidationError


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    jwt = db.Column(db.String)
    avatar_url = db.Column(db.String(256))
    passwd = db.Column(db.String(256))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    registration_token = db.Column(db.String(128))
    activated = db.Column(db.Integer, default=0)
    join_date = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    watched_movies = db.relationship('WatchedMovie', backref=db.backref('user', lazy='joined'), lazy='dynamic',
                                     cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref=db.backref('user', lazy='joined'), lazy='dynamic',
                               cascade='all, delete-orphan')
    
    def __init__(self):
        self.image_base64 = None
    
    def get_url(self):
        return url_for('user_controllers.get_user', user_id=self.user_id, _external=True)
    
    def export_data(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'join_date': self.join_date.isoformat() + 'Z',
            'watched_movies': url_for('user_controllers.get_watched_movies', user_id=self.user_id, _external=True)
        }
    
    def import_data(self, data):
        try:
            self.login = data['login']
            self.email = data['email']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.passwd = generate_password_hash(data['passwd'])
            self.image_base64 = data['avatar64']
            # print(data['avatar64'])
        except KeyError as e:
            raise ValidationError('Invalid user: missing ' + e.args[0])
    
    def modify_data(self, data):
        if 'login' in data:
            self.login = data['login']
        if 'email' in data:
            self.email = data['email']
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'passwd' in data:
            self.passwd = data['passwd']
    
    def exists(self):
        login_exists = User.query.filter_by(login=self.login).first()
        email_exists = User.query.filter_by(email=self.email).first()
        if login_exists or email_exists:
            return True
        return False
    
    def create_userfolder(self):
        os.mkdir(current_app.config['ROOT_DIRECTORY'] + '/static/users/' + self.login)
    
    def save_img(self):
        if self.image_base64 is None:
            return
        im = Image.open(BytesIO(base64.b64decode(self.image_base64.split(',')[1])))
        im_filename = str(uuid.uuid4()) + '.' + im.format
        im_dbpath = '/static/' + self.login + '/' + im_filename
        im_filepath = os.path.join(current_app.config['ROOT_DIRECTORY'],
                                   'static', 'users', self.login, im_filename)
        im.save(im_filepath)
        self.avatar_url = im_dbpath
    
    def send_confirm_email(self):
        token = str(uuid.uuid4())
        subject = 'Hypertube email confirmation'
        sender = 'http://localhost:4200/'
        recipient = self.email
        body = '''Greetings new hypertube user!
        \n\nPlease follow the link to finish registration:
        \n{0}'''.format(current_app.config['NG_ADDRESS']
                        + '/sign-in/?confirmed=true&token=' +
                        token +
                        '&login=' +
                        self.login)
        msg = Message(sender=sender,
                      recipients=[recipient],
                      subject=subject,
                      body=body
                      )
        self.registration_token = token
        mail.send(msg)
    