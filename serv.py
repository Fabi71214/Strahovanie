import os
import logging
<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, jsonify
import smtplib
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
BOT_TOKEN = '7961369773:AAGY0RkHAmsRVdGAN0GtAHOqXJNijmjHRUs'
telegram_bot = telebot.TeleBot(BOT_TOKEN)
=======
from flask import Flask, render_template, request, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

>>>>>>> b0c15ba4648226fe8c18a86f74f21d9e6ebefde0
ap = Flask(__name__)
ap.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key-for-development')
UPLOAD_FOLDER = 'uploads'
ap.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@ap.route("/")
def index():
    return render_template("strahovka.html")

@ap.route("/messg", methods=["POST"])
def send_message():
<<<<<<< HEAD
    
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
=======
    try:
        name = request.form.get("name", "").strip()
        tel = request.form.get("tel", "").strip()
        gmail = request.form.get("gmail", "").strip()
        mas = request.form.get("mes", "").strip()
        
        logger.info(f"Получены данные: {name}, {tel}, {gmail}, {mas}")
        
        # Проверка обязательных полей
        if not name or not tel:
            logger.error("Не заполнены обязательные поля")
            return render_template("strahovka.html", error="Заполните имя и телефон")
        
        mess_text = f"Была отправлена заявка с сайта.\nИмя: {name}\nТелефон: {tel}\nПочта: {gmail}\nСообщение: {mas}"
        
        success = send_msndr_email("farbi89@yandex.ru", "Заявка с сайта", mess_text)
        
        if success:
            logger.info("Письмо успешно отправлено")
            return render_template("strahovka.html", success=True)
        else:
            logger.error("Ошибка при отправке письма")
            return render_template("strahovka.html", error="Ошибка отправки, попробуйте позже")
            
    except Exception as e:
        logger.error(f"Ошибка в обработчике: {str(e)}")
        return render_template("strahovka.html", error="Произошла ошибка")

def send_msndr_email(to_email, subject, message_text):
    try:
        # Используем переменные окружения для безопасности
        smtp_server = os.environ.get('SMTP_SERVER', "smtp.msndr.net")
        port = int(os.environ.get('SMTP_PORT', 587))
        username = os.environ.get('EMAIL_USER', "farbi89@yandex.ru")
        password = os.environ.get('EMAIL_PASSWORD', "89698e2439f9911d39a259f161c61727")
        
        logger.info(f"Подключаемся к SMTP: {smtp_server}:{port}")
        
        # Создание сообщения
        message = MIMEMultipart()
        message['From'] = username
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(message_text, 'plain', 'utf-8'))
        
        # Подключение к серверу
        server = smtplib.SMTP(smtp_server, port, timeout=30)
        server.set_debuglevel(1)  # Включаем подробное логирование SMTP
        
        server.starttls()  # Включаем шифрование
        server.login(username, password)
        
        logger.info("Авторизация успешна, отправляем письмо...")
        
        text = message.as_string()
        server.sendmail(username, to_email, text)
        server.quit()
        
        logger.info("Письмо успешно отправлено!")
        return True
        
    except smtplib.SMTPException as e:
        logger.error(f"SMTP ошибка: {e}")
        return False
    except Exception as e:
        logger.error(f"Общая ошибка при отправке: {e}")
        return False
>>>>>>> b0c15ba4648226fe8c18a86f74f21d9e6ebefde0
