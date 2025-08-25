import telebot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN

from db import db

import re


bot = telebot.TeleBot(TOKEN)


def get_next_question(current=0):
    question = db.get_next_question(current)
    answers = db.get_answers(question.id)
    markup = InlineKeyboardMarkup()
    for answer in answers:
        markup.add(
            InlineKeyboardButton(text=answer.text, callback_data=f'question_id={question.id}&answer_id={answer.id},'))
    return question, markup

@bot.message_handler(commands=['start'])
def start(message):
    question, markup = get_next_question()

    bot.send_message(message.chat.id, 'We start')
    bot.send_message(message.chat.id, question.text, reply_markup=markup)


def filter_answers(callback):
    data = callback.data
    res = re.search(r'^question_id=\d+', data)
    return res
@bot.callback_query_handler(func=filter_answers)
def check_answer(callback):
    data = callback.data
    res = re.findall(r'question_id=(\d+)&answer_id=(\d+)',data)[0]
    question_id = int(res[0])
    answer_id = int(res[1])
    checker = db.check_answer(question_id, answer_id)
    if checker:
        bot.send_message(callback.message.chat.id,'Good')
    else:
        bot.send_message(callback.message.chat.id,'NGood')
    try:
        question, markup = get_next_question(question_id)

        if question:
            bot.send_message(callback.message.chat.id, question.text, reply_markup=markup)
        else:
            bot.send_message(callback.message.chat.id, 'end')
    except AttributeError:
        bot.send_message(callback.message.chat.id, 'Quiz_end')




bot.infinity_polling()


# @bot.callback_query_handler(func=lambda call: True)
# def check_answer(call):
#     answer_id = int(call.data) #ID
#     # Получаем текущий вопрос (нужно хранить его где-то, например, в user_data или базе)
#     question = db.get_current_question(call.message.chat.id)
#     correct_answer = db.get_correct_answer(question.id)  # возвращает объект ответа или его ID
#
#     if answer_id == correct_answer.id:
#         bot.answer_callback_query(call.id, "Правильно!")
#     else:
#         bot.answer_callback_query(call.id, "Неправильно.")



