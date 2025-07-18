# -*- coding: utf-8 -*-
"""
Created at: 15.07.2025
@author: marteszibellina
Filename: __init__
App: ~/Dev/Ollama/ollama-flask/ollama-gui/__init__.py
"""

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import bp as main_bp  # ingore

    app.register_blueprint(main_bp)

    return app
