import telebot
from config import TOKEN
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import json
import requests
from API_AI import YandexGPT



class Chat:
    def __init__(self,bot):
        self.i_ask = None
        self.i_repeat = None
        self.bot = bot
        self.bot.message_handler(commands=['start', 'help'])(self.send_welcome)
        self.bot.message_handler(commands=['AI'])(self.send_quest)
        self.check = 0
        self.bot.callback_query_handler(func=lambda call: True)(self.handle_query)


    def send_welcome(self, message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        inline_start = InlineKeyboardMarkup()
        inline_start.add(InlineKeyboardButton(text='Данное сообщение', callback_data='/help'),InlineKeyboardButton(text='Ask AI', callback_data='/AI'))
        markup.add(KeyboardButton("/help"), KeyboardButton("/AI"))
        bot.send_message(message.chat.id, 'Список команд\n/help - данное сообщение\n/AI - ask ai', reply_markup = inline_start)


    def handle_query(self, call):
        if call.data == '/help':
            self.send_welcome(call.message)
        elif call.data == '/AI':
            self.send_quest(call.message)
        else:
            self.bot.answer_callback_query(call.id, "Неизвестная команда")


    def send_quest(self,message):
        bot.reply_to(message, 'I translate')
        bot.register_next_step_handler(message,self.get_translate)
    def get_translate(self,message):
        jandex = YandexGPT()
        question = jandex.get_answer(text=self.i_ask)
        bot.send_message(message.chat.id,f'Good: \n {question} ')

if __name__ == '__main__':
    bot = telebot.TeleBot(TOKEN)
    chat = Chat(bot)
    bot.infinity_polling()


