# app/__init__.py
from flask import Flask
from app.config import Config
from dotenv import load_dotenv

load_dotenv()    # <-- this will populate os.environ from .env

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Register blueprints.
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
