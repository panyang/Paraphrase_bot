# -*- coding: utf-8 -*-

import telebot
import config
bot = telebot.TeleBot(config.token)

class DatabaseInteraction:
    """ Класс взаимодействия с базой данных"""

    def connect(self, connection_string):
        """ Подключиться по connection_string"""
        print('Connecting ({}) ...'.format(connection_string))

    def getFact(self):
        """Получить факт"""
        print('Fact')
        return 'X работает в Y'

    def getRandomPeriphrase(self):
        """ Получить рандомный перифраз"""
        print('Random periphrase')
        return '<strong>ПЕРСОНА</strong> предоставляет услуги по ремонту машин в <strong>ОРГАНИЗАЦИЯ</strong>'

    def saveResult(self, result):
        """ Сохранить результат перифраза, предложенный пользователем, в базе данных"""
        print('Saving result ({}) ...'.format(result))

    def disconnect(self):
        """ Отключиться"""
        print('Disconnecting...')

    def __init__(self):
        """ Конструктор"""
        print('Initializing database stub object')

db = DatabaseInteraction()

@bot.message_handler(commands = ['start', 'help'])
def send_message(message):
    """ Приветственное сообщение. """
    bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /create. Вы увидите предложение, которое нужно будет перефразировать.')

@bot.message_handler(commands = ['create'])
def create(message):
    """ При выборе команды create пользователь получает рандомный перифраз. """
    bot.send_message(message.chat.id, parse_mode='HTML', text = db.getRandomPeriphrase())

@bot.message_handler(func=lambda message: True, content_types=['text']) #здесь надо команда пробел + предложение
def me(message):
    """ Пользователь вводит перифраз, который потом записывается в базу данных. """
    # Проверка на наличие участников
    if 'ПЕРСОНА' and 'ОРГАНИЗАЦИЯ' in message.text.split(' '):
        db.saveResult(message.text)
        bot.send_message(message.chat.id, 'Спасибо, Ваш ответ записан')
        # Если ответ записан, то должен быть выход из функции
    else:
        bot.send_message(message.chat.id, 'Вы не использовали обязательных участников')

# @bot.message_handler(commands = ['verify'])
# def verify():
#     """Верификация перифразов, предложенных другими пользователями. Нужно на кнопках выбрать да или нет"""
#     bot.send_message(message.chat.id, parse_mode='HTML', text = db.getRandomPeriphrase())

if __name__ == '__main__':
    # bot.set_update_listener(listener)
    bot.polling(none_stop=True)
    while True:
        time.sleep(200)
