from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import sqlite3
from pathlib import Path
import app.keyboards as kb

router = Router()

DB_PATH = str(Path(__file__).with_name("tasker.db"))

class NoteState:
    def __init__(self):
        self.waiting_for_note = False

note_state = NoteState()

# Инициализация БД
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS note (
            tg_id INTEGER,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

init_db()

# ——— utils ———
def norm(text: str | None) -> str:
    return (text or "").strip().lower()

async def send_long(message: Message, text: str, chunk=4000):
    for i in range(0, len(text), chunk):
        await message.answer(text[i:i+chunk])

# ——— handlers ———

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет! Ваш ID: {message.from_user.id}\n"
        "Используйте кнопки для работы с заметками",
        reply_markup=kb.main
    )

# INFO (регистронезависимо)
@router.message(F.text.func(lambda t: norm(t) == "info"))
async def cmd_info(message: Message):
    await message.answer("Бот для заметок. Функционал: добавить/показать/удалить заметки.")

# ADD TASK (регистронезависимо)
@router.message(F.text.func(lambda t: norm(t) == "add task"))
async def cmd_add_task(message: Message):
    note_state.waiting_for_note = True
    await message.answer("Введите текст заметки:")

# Сохранение заметки — сработает ТОЛЬКО когда ждём ввод
@router.message(lambda m: note_state.waiting_for_note and bool(norm(m.text)))
async def save_task_text(message: Message):
    note_state.waiting_for_note = False  # сбрасываем флаг
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO note (tg_id, name) VALUES (?, ?)",
                (message.from_user.id, message.text.strip())
            )
            conn.commit()
        await message.answer("✅ Заметка сохранена!")
    except sqlite3.Error as e:
        await message.answer(f"❌ Ошибка БД: {e}")

# SHOW (регистронезависимо)
@router.message(F.text.func(lambda t: norm(t) == "show"))
async def cmd_show(message: Message):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, created_at FROM note WHERE tg_id = ? ORDER BY created_at DESC",
                (message.from_user.id,)
            )
            notes = cursor.fetchall()
    except sqlite3.Error as e:
        await message.answer(f"❌ Ошибка БД: {e}")
        return

    if not notes:
        await message.answer("📭 У вас пока нет заметок.")
        return

    lines = ["📋 Ваши заметки:", ""]
    for idx, (name, created_at) in enumerate(notes, start=1):
        lines.append(f"{idx}. {name}  🕒 {created_at}")
    text = "\n".join(lines)

    if len(text) > 4000:
        await send_long(message, text)
    else:
        await message.answer(text)

# Опционально: мягкий ответ на прочие сообщения (НЕ перехватывает команды)
@router.message()
async def fallback(message: Message):
    # ничего не делаем, чтобы не мешать другим хэндлерам
    # можно подсказать пользователю:
    # await message.answer("Не понял. Нажмите кнопку или введите: Add task / SHOW / INFO")
    pass
