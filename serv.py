import os
import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify
import smtplib
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
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
    
    name = request.form.get("name", "").strip()
    tel = request.form.get("tel", "").strip()
    gmail = request.form.get("gmail", "").strip()
    mas = request.form.get("mes", "").strip()
        
    # Проверка обязательных полей
    if not name or not tel:
        return render_template("strahovka.html", error="Заполните имя и телефон")
    else:
        mess_text = f"Была отправлена заявка с сайта Страхования:\nИмя: {name}\nТелефон: {tel}\nПочта: {gmail}\nСообщение: {mas}"
        aa=open("C:/Users/user/Desktop/Program_Progekt/3D_Gallery/id_tg.txt","r")
        statik=aa.readlines()
        for n in statik:
            telegram_bot.send_message(n,mess_text)
        return redirect(url_for('index'))
if __name__ == "__main__":
    ap.run(host='0.0.0.0', port=5454, debug=False, use_reloader=False)
