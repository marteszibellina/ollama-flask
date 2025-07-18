# -*- coding: utf-8 -*-
"""
Created at: 16.07.2025
@author: marteszibellina
Filename: models
App: ~/Dev/Ollama/ollama-flask/ollama-gui/models.py
"""


from datetime import datetime

from app import db


class Conversation(db.Model):
    """
    Conversation model
    """
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), index=True)
    user_input = db.Column(db.Text)
    ai_response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Conversarion {self.session_id}>'
