# import os
# import sys
# from datetime import timedelta
#
# from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
# from flask_moment import Moment
#
# from app.blueprints import index_blueprint, auth_blueprint
#
# """ Necesario para incluir el folder templanes en pyinstaller"""
# if getattr(sys, 'frozen', False):
#     template_folder = os.path.join(sys._MEIPASS, 'templates')
#     app = Flask(__name__, template_folder=template_folder)
# else:
#     app = Flask(__name__)
#
# app.register_blueprint(index_blueprint)
# app.register_blueprint(auth_blueprint)
#
# app.config['SECRET_KEY'] = 'llavedeprueba'
# app.config['SEED_ADMIN_EMAIL'] = 'llavedeprueba'
# app.config['SEED_ADMIN_PASSWORD'] = 'llavedeprueba'
# app.config['REMEMBER_COOKIE_DURATION'] = timedelta(hours=1)
#
# moment = Moment(app)
# toolbar = DebugToolbarExtension(app)


from app import create_app, db
from app.models import User, Role

app = create_app('dev')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


if __name__ == '__main__':
    app.run(DEBUG=True)
