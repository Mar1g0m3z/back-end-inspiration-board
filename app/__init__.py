from flask import Flask
from flask_cors import CORS
import os
from .db import db, migrate
from .models import board, card
from app.routes.card_routes import bp as cards_bp
from app.routes.board_routes import bp as boards_bp
# Import models, blueprints, and anything else needed to set up the app or database


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register Blueprints 
    app.register_blueprint(cards_bp)
    app.register_blueprint(boards_bp)

    CORS(app)
    return app
