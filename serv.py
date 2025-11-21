import os
from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
ap = Flask(__name__)
ap.secret_key = os.environ.get('SECRET_KEY', 'faljdhedurtdjjdtlback-secret-key-for-development')
UPLOAD_FOLDER = 'uploads'
ap.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@ap.route("/")
def index():
    return render_template("strahovka.html")

@ap.route("/messg", methods=["POST"])
def login():
    name = request.form.get("name")
    tel = request.form.get("tel")
    gmail=request.form.get("gmail")
    mas=request.form.get("mes")
    print(name,tel,gmail,mas)
    mess_text=f"Была отправленны заявка с сайта. Имя: {name} Телефон: {tel} Почта: {gmail} Соопщение: {mas}"
    send_msndr_email("farbi89@yandex.ru","Заявка",mess_text)
    return render_template("strahovka.html")

def send_msndr_email(to_email, subject, message_text):
    # Данные из вашего аккаунта msndr.net
    smtp_server = "smtp.msndr.net"
    port = 587  # STARTTLS
    username = "farbi89@yandex.ru"
    password = "89698e2439f9911d39a259f161c61727"
    
    # Создание сообщения
    message = MIMEMultipart()
    message['From'] = username
    message['To'] = to_email
    message['Subject'] = subject
    
    # Добавляем текст сообщения
    message.attach(MIMEText(message_text, 'plain', 'utf-8'))
    try:
        print("🔄 Подключаемся к серверу...")
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Включаем шифрование
        server.login(username, password)
        
        print("✅ Подключение успешно! Отправляем письмо...")
        text = message.as_string()
        server.sendmail(username, to_email, text)
        server.quit()
        
        print("✅ Письмо успешно отправлено через msndr.net!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False
    
if __name__ == "__main__":
    ap.run()