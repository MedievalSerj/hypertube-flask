import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join('..', basedir, 'data.sqlite')

NG_ADDRESS = 'http://localhost:4200'
ROOT_DIRECTORY = os.getcwd()
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
UPLOAD_FOLDER = '/nfs/2016/s/sladonia/repo/hypertube-flask/static/users'
SECRET_KEY = 'wilhelm-marduk'
DEBUG = True
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'ladonya.s@gmail.com'
MAIL_PASSWORD = os.environ.get('G_PASSWD')
