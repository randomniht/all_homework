import telebot
from config import TOKEN
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
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
    def send_welcome(self, message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add(KeyboardButton("/help"), KeyboardButton("/AI"))
        bot.send_message(message.chat.id, 'Список команд\n/help - данное сообщение\n/AI - ask ai', reply_markup=markup)

    def send_quest(self,message):
        bot.reply_to(message, 'In next message')
        bot.register_next_step_handler(message,self.get_message)
    def get_message(self,message):
        self.i_ask = message.text
        bot.send_message(message.chat.id,'Good, Ai repeat as ')
        bot.register_next_step_handler(message,self.get_author)

    def get_author(self,message):
        self.check += 1
        if self.check < 2:
            self.i_repeat = message.text
            jandex = YandexGPT()
            question = jandex.get_answer(text=self.i_ask, role=self.i_repeat)
            bot.send_message(message.chat.id,f'Good, quest: \n {question} ')
        else:
            bot.send_message(message.chat.id, f'U made a lot of requests')
            bot.register_next_step_handler(message, self.send_welcome)
if __name__ == '__main__':
    bot = telebot.TeleBot(TOKEN)
    chat = Chat(bot)
    bot.infinity_polling()


