# -*- coding: utf-8 -*-
"""
Created at: 16.07.2025
@author: marteszibellina
Filename: settings
App: ~/Dev/Ollama/ollama-flask/ollama-gui/settings.py
"""

import os

from dotenv import load_dotenv


class Config(object):
    """Настройки приложения"""
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
