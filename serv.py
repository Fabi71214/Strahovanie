import os
import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import telebot
import uvicorn
import sqlite3
from datetime import datetime
# логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = '7961369773:AAGY0RkHAmsRVdGAN0GtAHOqXJNijmjHRUs'
telegram_bot = telebot.TeleBot(BOT_TOKEN)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = 'uploads'


# Главная страница
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    analitik()
    return templates.TemplateResponse("strahovka.html", {"request": request})

def analitik():
    conn = sqlite3.connect("analik.db")
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    # есть ли уже запись за сегодня
    cursor.execute("""
                    SELECT visits
                    FROM visits_daily 
                    WHERE date = ?
                    """, (today,))
    row = cursor.fetchone()

    if row:
        # если есть — увеличиваем счетчик
        cursor.execute("""
        UPDATE visits_daily
        SET visits = visits + 1
        WHERE date = ?
        """, (today,))
    else:
        # если нет — создаем новую запись
        cursor.execute("""
        INSERT INTO visits_daily (date, visits)
        VALUES (?, 1)
        """, (today,))

        # проверяем сколько дней
        cursor.execute("SELECT COUNT(*) FROM visits_daily")
        count = cursor.fetchone()[0]

        if count > 7:
            # удаляем самый старый день
            cursor.execute("""
            DELETE 
            FROM visits_daily
            WHERE date = (
                SELECT date
                FROM visits_daily
                ORDER BY date ASC
                LIMIT 1
            )
            """)
    cursor.execute("""
                    SELECT *
                    FROM visits_daily
                        """)
    x=cursor.fetchone()
    print(x)
    conn.commit()
    conn.close()

# Обработка формы
@app.post("/messg")
async def send_message(
    request: Request,
    name: str = Form(...),
    tel: str = Form(...),
    gmail: str = Form(None),
    mes: str = Form(None)
):
    name = name.strip()
    tel = tel.strip()
    gmail = (gmail or "").strip()
    mes = (mes or "").strip()
    print(name,mes,tel)
    if not name or not tel:
        return templates.TemplateResponse(
            "strahovka.html",
            {"request": request, "error": "Заполните имя и телефон"}
        )

    mess_text = (
        f"Была отправлена заявка:\n"
        f"Имя: {name}\n"
        f"Телефон: {tel}\n"
        f"Почта: {gmail}\n"
        f"Сообщение: {mes}"
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    id_path = os.path.join(base_dir, "id_tg.txt")

    with open(id_path, "r", encoding="utf-8") as f:
        chat_ids = f.readlines()

    for chat_id in chat_ids:
        telegram_bot.send_message(chat_id.strip(), mess_text)

    return RedirectResponse(url="/", status_code=303)


def csk():
    conn= sqlite3.connect("analik.db")
    cursor=conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS visits_daily (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE,
    visits INTEGER DEFAULT 0
)
""")
    conn.commit()
    conn.close()
csk()
uvicorn.run(app,host="127.0.0.1",port=5000)