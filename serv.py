import os
import logging
from flask import Flask, render_template, request, redirect, url_for
import telebot

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = '7961369773:AAGY0RkHAmsRVdGAN0GtAHOqXJNijmjHRUs'
telegram_bot = telebot.TeleBot(BOT_TOKEN)

ap = Flask(__name__)
ap.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key-for-development')

UPLOAD_FOLDER = 'uploads'
ap.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@ap.route("/")
def index():
    return render_template("strahovka.html")


@ap.route("/messg", methods=["POST"])
def send_message():
    try:
        name = request.form.get("name", "").strip()
        tel = request.form.get("tel", "").strip()
        gmail = request.form.get("gmail", "").strip()
        mas = request.form.get("mes", "").strip()

        if not name or not tel:
            return render_template("strahovka.html", error="Заполните имя и телефон")

        mess_text = (
            f"Была отправлена заявка с сайта Страхования:\n"
            f"Имя: {name}\n"
            f"Телефон: {tel}\n"
            f"Почта: {gmail}\n"
            f"Сообщение: {mas}"
        )

        base_dir = os.path.dirname(os.path.abspath(__file__))
        id_path = os.path.join(base_dir, "id_tg.txt")

        with open(id_path, "r", encoding="utf-8") as f:
            chat_ids = f.readlines()

        for chat_id in chat_ids:
            telegram_bot.send_message(chat_id.strip(), mess_text)

        return redirect(url_for('index'))

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return render_template("strahovka.html", error="Произошла ошибка")


if __name__ == "__main__":
    ap.run(host='0.0.0.0', port=5454, debug=False, use_reloader=False)
