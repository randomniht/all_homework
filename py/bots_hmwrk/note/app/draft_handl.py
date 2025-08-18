from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import ContentType
import sqlite3
import app.keyboards as kb
router = Router()

def init_db():
    db = sqlite3.connect('tasker.db')

    c = db.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS note (
        tg_id INTEGER,
        name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    db.commit()

    db.close()

init_db()
class Config:
    def __init__(self):
        self.user_id = None
        self.name = None
config = Config()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Ку, вот что я могу, Ваш ID: {message.from_user.id}", reply_markup= kb.main)
    config.user_id = message.from_user.id
   




@router.message(F.text == 'INFO')
async def cmd_info(message: Message):
    await message.answer('Данный бот создан для заметок,  его функционал добавить/удалить заметку')

@router.message(F.text == 'Add task')
async def cmd_add_task(message: Message):
    config.user_id = message.from_user.id
    await message.answer("Текст заметки:")

@router.message()
async def save_task_text(message: Message):
    # Проверяем, что это нужный пользователь и следующий шаг активирован
    if config.user_id == message.from_user.id:
        task_text = message.text  # Текст заметки
        config.user_id = None  # Сбрасываем флаг
        config.name = task_text
        try:
            conn = sqlite3.connect('tasker.db')
            c = conn.cursor()
            c.execute(
                "INSERT INTO note (tg_id, name) VALUES (?, ?)",
                (config.user_id, config.name)
            )
            conn.commit()
            await message.answer("✅ Заметка сохранена!")
        except sqlite3.Error as e:
            await message.answer(f"❌ Ошибка БД: {e}")
        finally:
            conn.close()
            config.user_id = None  # Сбрасываем состояние
@router.message(F.text == 'SHOW')  # Команда для показа заметок
async def show_notes(message: Message):
    try:
        # Подключаемся к БД
        conn = sqlite3.connect('tasker.db')
        cursor = conn.cursor()
        
        # Достаем все заметки пользователя
        cursor.execute(
            "SELECT name, created_at FROM note WHERE tg_id = ? ORDER BY created_at DESC",
            (message.from_user.id,)
        )
        notes = cursor.fetchall()
        
        if not notes:
            await message.answer("У вас нет заметок!")
            return
        notes_text = "\n".join(
            [f"📌 {note[0]} (дата: {note[1]})" for note in notes]
        )
        await message.answer(f"Ваши заметки:\n{notes_text}")
        
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
    finally:
        conn.close()

