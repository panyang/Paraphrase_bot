# -*- coding: utf-8 -*-

import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.token)


class DatabaseInteraction:
    """ Класс взаимодействия с базой данных"""

    def connect(self, connection_string):
        """ Подключиться по connection_string"""
        print('Connecting ({}) ...'.format(connection_string))

    def get_fact(self):
        """Получить факт"""
        print('Fact')
        return 'X работает в Y'

    def get_random_periphrase(self):
        """ Получить рандомный перифраз"""
        print('Random periphrase')
        return '<strong>ПЕРСОНА</strong> предоставляет услуги по ремонту машин в <strong>ОРГАНИЗАЦИЯ</strong>'

    def save_result(self, result):
        """ Сохранить результат перифраза, предложенный пользователем, в базе данных"""
        print('Saving result ({}) ...'.format(result))

    def disconnect(self):
        """ Отключиться"""
        print('Disconnecting...')

    def __init__(self):
        """ Конструктор"""
        print('Initializing database stub object')

db = DatabaseInteraction()

markup = types.ReplyKeyboardMarkup()
markup.row('/create', '/verify')
markup.row('/start', '/help')

PERIPHRASE_CREATE = 0
PERIPHRASE_CREATED = 1
PERIPHRASE_VERIFY = 3
PERIPHRASE_VERIFIED = 4

periphrase_step = {}


@bot.message_handler(commands=['start', 'help'])
def send_message(message):
    """ Приветственное сообщение. """
    bot.send_message(message.chat.id, "Выберите:", reply_markup=markup)  # Пользовательская клавиатура
    bot.send_message(message.chat.id, 'Привет, я FactCollector! '
                                      'Выбери команду /create, чтобы перефразировать предложение. Выбери команду '
                                      '/verify, чтобы подтвердить предложение')


@bot.message_handler(commands=['create'])
def create(message):
    """ При выборе команды create пользователь получает рандомный перифраз. """
    bot.send_message(message.chat.id, 'Сейчас Вы увидите предложение,'
                                      ' которое нужно будет перефразировать. Введите, пожалуйста, предложение, '
                                      'содержащее отношение между участниками данной ситуации')
    bot.send_message(message.chat.id, parse_mode='HTML', text=db.get_random_periphrase())
    periphrase_step[message.chat.id] = PERIPHRASE_CREATE


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == PERIPHRASE_CREATE)
def me_create(message):
    """ Пользователь вводит перифраз, который потом записывается в базу данных. """
    # Проверка на наличие участников
    if 'ПЕРСОНА' and 'ОРГАНИЗАЦИЯ' in message.text.split(' '):
        db.save_result(message.text)
        keyboard_hider = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, 'Спасибо, Ваш ответ записан')  # reply_markup=keyboard_hider) убираем клаву
        periphrase_step[message.chat.id] = PERIPHRASE_CREATED
    else:
        bot.send_message(message.chat.id, 'Вы не использовали обязательных участников')


@bot.message_handler(commands=['verify'])
def verify(message):
    """Верификация перифразов, предложенных другими пользователями. Нужно на кнопках выбрать да или нет"""
    bot.send_message(message.chat.id, parse_mode='HTML', text='Сейчас Вы увидите предложение,которое нужно будет '
                                                              'оценить. Введите <strong>ДА</strong>, '
                                                              'если предложение содержит факт, и <strong>НЕТ</strong>, '
                                                              'если не содержит')
    # Сделать кастомную клавиатуру и больше выборов (подтвердить/содержит), выделить жирным
    bot.send_message(message.chat.id, parse_mode='HTML', text=db.get_random_periphrase())
    periphrase_step[message.chat.id] = PERIPHRASE_VERIFY


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == PERIPHRASE_VERIFY)
def me_verify(message):
    """ Пользователь вводит перифраз, который потом записывается в базу данных. """
    # Проверка на наличие участников
    if 'ДА' or 'НЕТ' in message.text.split(' '):
        db.save_result(message.text)
        keyboard_hider = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, 'Спасибо, Ваш ответ записан')
        # Если ответ записан, то должен быть выход из функции
        periphrase_step[message.chat.id] = PERIPHRASE_VERIFIED
    else:
        bot.send_message(message.chat.id, 'Вы не использовали обязательных участников')

if __name__ == '__main__':
    # bot.set_update_listener(listener)
    bot.polling(none_stop=True)
    while True:
        time.sleep(200)

# me только во включенном режиме create, и для verify то же самое
# Разрешать получать только один ответ
