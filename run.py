#!/usr/bin/env python
from app import create_app
from app import db
import os
import sys
from app.users.user_model import User


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cfg = sys.argv[1]
    else:
        cfg = 'development'
    app = create_app(cfg)
    if not os.path.exists('./static/users'):
        os.mkdir('./static/users')
    with app.app_context():
        db.create_all()
        if User.query.get(1) is None:
            user = User()
            data = {
              'login': 'kotlin',
               'email': 'ladonya.s@gmail.com',
              'first_name': 'Kotlin',
              'last_name': 'Jackson',
              'passwd': '1234567q',
              'avatar64': None
            }
            user.import_data(data)
            db.session.add(user)
            db.session.commit()
    app.run()
