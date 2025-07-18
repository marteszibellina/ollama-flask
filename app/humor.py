# -*- coding: utf-8 -*-
"""
Created at: 17.07.2025
@author: marteszibellina
Filename: humor
App: ~/Dev/Ollama/ollama-flask/app/humor.py
"""

import json
import random


def load_humor(filename="humor.json"):
    """Загружает юмор из файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            humor = json.load(f)
        return humor
    except FileNotFoundError:
        return {}

def generate_joke(choice="random", humor_file="humor.json"):
    """Генерирует шутку определенного типа."""
    humor = load_humor(humor_file)
    if choice == "random":
        choice = random.choice(list(humor.keys()))
    if choice in humor and humor[choice]:
        return random.choice(humor[choice])
    return "Извините, у меня нет шуток этого типа."

# load_humor()
