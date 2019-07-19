from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from app.config import config

moment = Moment()
# debug_toolbar = DebugToolbarExtension()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    # Carga clase config
    app.config.from_object(config[config_name])

    # Inicializa las extensiones
    config[config_name].init_app(app)
    moment.init_app(app)
    # debug_toolbar.init_app(app)
    db.init_app(app)
    # Si se utiliza create_all, especificar bind=None para que solo afecte a la DB principal y no a los binds
    # db.create_all(app=app, bind=None)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Registra blueprints

    from .index import index_blueprint
    app.register_blueprint(index_blueprint)
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .dashboard import dash_blueprint
    app.register_blueprint(dash_blueprint, url_prefix='/dash')

    # Attach routes and custom error pages here
    return app
