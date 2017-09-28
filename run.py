#!/usr/bin/env python
from app import create_app
from app import db
import os
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cfg = sys.argv[1]
    else:
        cfg = 'development'
    app = create_app(cfg)
    with app.app_context():
        db.create_all()
    if not os.path.exists('./static/users'):
        os.mkdir('./static/users')
    app.run()
