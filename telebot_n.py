# -*- coding: utf-8 -*-

import telebot
import config
bot = telebot.TeleBot(config.token)

class DatabaseInteraction:
    """Класс взаимодействия с базой данных"""

    def connect(self, connection_string):
        """Подключиться по connection_string"""
        print('Connecting ({}) ...'.format(connection_string))

    def getFact(self):
        """Получить факт"""
        print('Fact')
        return 'X работает в Y'

    def getRandomPeriphrase(self):
        """Получить рандомный перифраз"""
        print('Random periphrase')
        return '<b>X</b> предоставляет услуги по ремонту машин в <b>Y</b>'

    def saveResult(self, result):
        """Сохранить результат перифраза, предложенный пользователем, в базе данных"""
        print('Saving result ({}) ...'.format(result))

    def disconnect(self):
        """Отключиться"""
        print('Disconnecting...')

    def __init__(self):
        """Конструктор"""
        print('Initializing database stub object')

db = DatabaseInteraction()

@bot.message_handler(commands = ['start', 'help'])
def send_message(message):
    bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /create. Вы увидите предложение, которое нужно будет перефразировать.')

@bot.message_handler(commands = ['create'])
def create(message):
    bot.send_message(message.chat.id, db.getRandomPeriphrase())

@bot.message_handler(func=lambda message: True, content_types=['text'])
def me(message):
    bot.send_message(message.chat.id, message.text)

# def listener(messages):
# 	for m in messages:
# 		if m.content_type == 'text':
# 			bot.send_message(m.chat.id, m.text)

if __name__ == '__main__':
    # bot.set_update_listener(listener)
    bot.polling(none_stop=True)
    while True:
        time.sleep(200)
