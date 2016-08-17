# -*- coding: utf-8 -*-

import telebot
import config
from telebot import types
from database import DatabaseInteraction

bot = telebot.TeleBot(config.token)
db = DatabaseInteraction()

# Создание кастомной клавиатуры
markup = types.ReplyKeyboardMarkup()
markup.row('/create', '/verify')
markup.row('/start', '/help')

markup_y_n = types.ReplyKeyboardMarkup()
markup_y_n.row('ДА', 'НЕТ')

PERIPHRASE_CREATE = 'create'
PERIPHRASE_CREATED = 'created'
PERIPHRASE_VERIFY = 1       # четное число
PERIPHRASE_VERIFIED = 2     # нечетное число

PERIPHRASE_CHECK = 'check'
PERIPHRASE_CHECKED = 'checked'

periphrase_step = {}


@bot.message_handler(commands=['start', 'help'])
def send_message(message):
    """
    Приветственное сообщение.
    """
    bot.send_message(message.chat.id, 'Привет, я FactCollector! '
                                      'Выбери команду /create, чтобы перефразировать предложение. Выбери команду '
                                      '/verify, чтобы подтвердить предложение', reply_markup=markup)


@bot.message_handler(commands=['create'])
def create(message):
    """
    При выборе команды create пользователь получает рандомный перифраз.
    """
    bot.send_message(message.chat.id, 'Сейчас Вы увидите предложение,'
                                      ' которое нужно будет перефразировать. Введите, пожалуйста, предложение, '
                                      'содержащее отношение между участниками данной ситуации')
    bot.send_message(message.chat.id, parse_mode='HTML', text=db.get_random_periphrase())
    periphrase_step[message.chat.id] = PERIPHRASE_CREATE


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == PERIPHRASE_CREATE)
def me_create(message):
    """
    Пользователь вводит перифраз, который потом записывается в базу данных.
    """
    # Проверка на наличие участников
    if 'ПЕРСОНА' and 'ОРГАНИЗАЦИЯ' in message.text.split(' '):
        db.save_result(message.text)
        # keyboard_hider = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, 'Спасибо, Ваш ответ записан')  # reply_markup=keyboard_hider) убираем клаву
        periphrase_step[message.chat.id] = PERIPHRASE_CREATED
    else:
        bot.send_message(message.chat.id, 'Вы не использовали обязательных участников')
    # Добавить проверку на оригинальность


@bot.message_handler(commands=['verify'])
def verify(message):
    """
    Верификация перифразов, предложенных другими пользователями. Нужно на кнопках выбрать да или нет.
    """
    bot.send_message(message.chat.id, parse_mode='HTML', text='Сейчас Вы увидите предложение,которое нужно будет '
                                                              'оценить. Введите <strong>ДА</strong>, '
                                                              'если предложение содержит факт, и <strong>НЕТ</strong>, '
                                                              'если не содержит', reply_markup=markup_y_n)
    # Сделать кастомную клавиатуру и больше выборов (подтвердить/содержит), выделить жирным
    bot.send_message(message.chat.id, parse_mode='HTML', text=db.get_random_periphrase())
    periphrase_step[message.chat.id] = PERIPHRASE_VERIFY
    # где-то надо прописывать, какой именно факт


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == PERIPHRASE_VERIFY)
def me_verify(message):
    """
    Пользователь вводит перифраз, который потом записывается в базу данных.
    """
    # Проверка на наличие участников
    if 'ДА' or 'НЕТ' in message.text.split(' '):
        db.save_value(message.text)
        # keyboard_hider = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, 'Спасибо, Ваш ответ записан', reply_markup=markup)
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
