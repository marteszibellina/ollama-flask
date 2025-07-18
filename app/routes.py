# -*- coding: utf-8 -*-
"""
Created at: 17.07.2025
@author: marteszibellina
Filename: routes
App: ~/Dev/Ollama/ollama-flask/app/routes.py
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

import ollama
from flask import Blueprint, jsonify, request, session

from app import db
from app.models import Conversation

bp = Blueprint("main", __name__)

# Настройка логгера
logger = logging.getLogger("ollama_thoughts")
logger.setLevel(logging.INFO)


class ThoughtLoggerFormatter(logging.Formatter):
    """Кастомный форматтер для логирования мыслей"""

    def format(self, record):
        thought_types = {
            "user_input": "👤: ",
            "system": "⚙️: ",
            "thinking": "💭: ",
            "response": "🗨️: ",
            "error": "❌: ",
        }
        if hasattr(record, "thought_type"):
            prefix = thought_types.get(record.thought_type, "")
            return f"[{datetime.now().strftime('%H:%M:%S')}] {prefix}{record.msg}"
        return super().format(record)


# Добавляем обработчик
handler = logging.StreamHandler()
handler.setFormatter(ThoughtLoggerFormatter())
logger.addHandler(handler)


def log_thought(thought_type: str, message: str):
    """Логирование с типом мысли"""
    extra = {"thought_type": thought_type}
    logger.info(message, extra=extra)


def extract_content(response) -> str:
    """Извлечение контента из ответа Ollama"""
    if hasattr(response, "message") and hasattr(response.message, "content"):
        return response.message.content
    elif isinstance(response, dict):
        return response.get("message", {}).get("content", str(response))
    return str(response)


def prepare_messages(prompt: str, conversation_history: List[Dict]) -> List[Dict]:
    """Подготовка сообщений для модели с логированием"""
    messages = []

    # Системное сообщение
    system_msg = {
        "role": "system",
        "content": 'Отвечай просто, без формальностей, можно на "ты". Поддерживай Markdown.',
    }
    messages.append(system_msg)
    log_thought("system", f"Системный промпт: {system_msg['content'][:50]}...")

    # История диалога
    if conversation_history:
        log_thought(
            "thinking", f"Загружаю историю ({len(conversation_history)} сообщений)"
        )
        for msg in conversation_history[-10:]:
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["ai"]})
            log_thought("context", f"{msg['user'][:30]}... → {msg['ai'][:30]}...")

    # Текущий запрос
    messages.append({"role": "user", "content": prompt})
    log_thought("thinking", f"Добавлен текущий запрос ({len(prompt)} символов)")

    return messages


def generate_ai_response(
    prompt: str, conversation_history: Optional[List[Dict]] = None
) -> str:
    """Генерация ответа с полным логированием процесса"""
    try:
        # Логируем входные данные
        log_thought("user_input", prompt[:200] + ("..." if len(prompt) > 200 else ""))

        # Подготовка контекста
        messages = prepare_messages(prompt, conversation_history or [])

        log_thought("thinking", "Начинаю генерацию ответа...")

        # Вариант 1: Официальный клиент Ollama
        try:
            log_thought("system", "Использую Ollama API (модель: gemma3n)")
            response = ollama.chat(
                model="gemma3n",
                messages=messages,
                options={"temperature": 0.7, "num_predict": 4096},
                stream=False,
            )

            # Обработка ответа
            result = extract_content(response)
            log_thought(
                "response",
                f"Сгенерирован ответ ({len(result)} символов): {result[:100]}...",
            )
            return result

        except Exception as e:
            log_thought("error", f"Ollama API: {str(e)}")
            raise

    except Exception as e:
        log_thought("error", f"Ошибка генерации: {str(e)}")
        return f"Ошибка: {str(e)}"


@bp.route("/chat", methods=["POST"])
def chat():
    """Обработчик чат-запросов с полным логированием"""
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        log_thought("error", "Пустой запрос")
        return jsonify({"error": "Пустой запрос"}), 400

    try:
        # Получаем историю
        convs = (
            Conversation.query.filter_by(session_id=session["session_id"])
            .order_by(Conversation.timestamp.desc())
            .limit(10)
            .all()
        )

        history = [{"user": c.user_input, "ai": c.ai_response} for c in reversed(convs)]

        # Генерация ответа
        ai_response = generate_ai_response(user_input, history)

        # Сохранение
        conv = Conversation(
            session_id=session["session_id"],
            user_input=user_input,
            ai_response=ai_response,
        )
        db.session.add(conv)
        db.session.commit()

        log_thought("system", "Диалог сохранен в базу")
        return jsonify(
            {"response": ai_response, "timestamp": datetime.utcnow().isoformat()}
        )

    except Exception as e:
        log_thought("error", f"Ошибка обработки запроса: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/", methods=["GET", "POST"])
def index():
    """Главная страница"""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")


@bp.route("/history", methods=["GET"])
def get_history():
    """Получение истории с пагинацией"""
    if "session_id" not in session:
        return jsonify([])

    conversations = (
        Conversation.query.filter_by(session_id=session["session_id"])
        .order_by(Conversation.timestamp.asc())
        .all()
    )

    history = [
        {
            "user": conv.user_input,
            "ai": conv.ai_response,
            "time": conv.timestamp.isoformat(),
        }
        for conv in conversations
    ]

    return jsonify({"history": history})


@bp.route("/clear", methods=["POST"])
def clear_history():
    """Очистка истории текущей сессии"""
    Conversation.query.filter_by(session_id=session["session_id"]).delete()
    db.session.commit()
    return jsonify({"status": "success"})
