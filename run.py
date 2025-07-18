# -*- coding: utf-8 -*-
"""
Created at: 16.07.2025
@author: marteszibellina
Filename: run
App: ~/Dev/Ollama/ollama-flask/app/run.py
"""

from app import create_app

app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
