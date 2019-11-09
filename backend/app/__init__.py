from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # call init_app to complete initialization
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def save_and_commit(item):
    db.session.add(item)
    db.session.commit()
db.save = save_and_commit
