import telebot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN

from db import db



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])

def start(message):
    question = db.get_next_question()
    answers = db.get_answers(question.id)
    markup = InlineKeyboardMarkup()
    for answer in answers:
        markup.add(InlineKeyboardButton(text=answer.text,callback_data=answer.text))

    bot.send_message(message.chat.id, 'We start')
    bot.send_message(message.chat.id, question.text, reply_markup=markup)
bot.infinity_polling()