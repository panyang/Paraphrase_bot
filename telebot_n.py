# -*- coding: utf-8 -*-

import telebot
import config
from telebot import types
from database import DatabaseInteraction

bot = telebot.TeleBot(config.token)
db = DatabaseInteraction()

# Создание кастомной клавиатуры
markup = types.ReplyKeyboardMarkup()
markup.row('/create', '/verify', '/verify2')
markup.row('/start', '/help')

markup_y_n = types.ReplyKeyboardMarkup()
markup_y_n.row('ДА', 'НЕТ')

PERIPHRASE_CREATE = 'create'
PERIPHRASE_CREATED = 'created'
PERIPHRASE_VERIFY = 1
PERIPHRASE_VERIFIED = 2
PERIPHRASE_VERIFY2 = 3
PERIPHRASE_VERIFIED2 = 4

periphrase_step = {}


@bot.message_handler(commands=['start', 'help'])
def send_message(message):
    """
    Приветственное сообщение.
    """
    bot.send_message(message.chat.id, 'Привет, я FactCollector! '
                                      'Выбери команду /create, чтобы перефразировать предложение. Выбери команду '
                                      '/verify, чтобы подтвердить предложение, выбери команду /verify2, чтобы '
                                      'проверить себя.', reply_markup=markup)


@bot.message_handler(commands=['create'])
def create(message):
    """
    При выборе команды create пользователь получает рандомный перифраз.
    """
    bot.send_message(message.chat.id, 'Сейчас ты увидишь предложение,'
                                      ' которое нужно будет перефразировать. Введи предложение, '
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
        bot.send_message(message.chat.id, 'Спасибо, ответ записан')  # reply_markup=keyboard_hider) убираем клаву
        periphrase_step[message.chat.id] = PERIPHRASE_CREATED
    else:
        bot.send_message(message.chat.id, 'Ты не использовал обязательных участников')
    # Добавить проверку на оригинальность


@bot.message_handler(commands=['verify'])
def verify(message):
    """
    Верификация перифразов, предложенных другими пользователями. Нужно на кнопках выбрать да или нет.
    """
    bot.send_message(message.chat.id, parse_mode='HTML', text='Сейчас ты увидишь предложение, которое нужно будет '
                                                              'оценить. Нажми <strong>ДА</strong>, '
                                                              'если предложение содержит факт работы, и <strong>НЕТ</strong>, '
                                                              'если не содержит', reply_markup=markup_y_n)
    periphrase_step[message.chat.id] = PERIPHRASE_VERIFY
    what_to_check = db.get_random_periphrase()
    bot.send_message(message.chat.id, parse_mode='HTML', text=what_to_check)
    # где-то надо прописывать, какой именно факт


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == PERIPHRASE_VERIFY)
def me_verify(message):
    """
    Пользователь вводит ответ, который потом записывается в базу данных.
    """
    what_to_check = db.get_random_periphrase()  # !!!!!
    # bot.send_message(message.chat.id, parse_mode='HTML', text=what_to_check)
    # Проверка на наличие участников
    if 'ДА' in message.text.split(' '):
        periphrase_points = db.get_periphrase_points(what_to_check)
        periphrase_points += 1
        db.save_periphrase_points(periphrase_points)
        bot.send_message(message.chat.id, 'Спасибо, ответ записан', reply_markup=markup)
        periphrase_step[message.chat.id] = PERIPHRASE_VERIFIED
    elif 'НЕТ' in message.text.split(' '):
        periphrase_points = db.get_periphrase_points(what_to_check)
        periphrase_points -= 1
        db.save_periphrase_points(periphrase_points)
        # keyboard_hider = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, 'Спасибо, ответ записан', reply_markup=markup)
        periphrase_step[message.chat.id] = PERIPHRASE_VERIFIED
    else:
        bot.send_message(message.chat.id, 'Ты не использовал обязательных участников')


@bot.message_handler(commands=['verify2'])
def verify_check(message):
    """
    Верификация перифразов, про которые мы точно знаем, содержится в них факт или нет. Нужно для проверки пользователя
    'на вшивость'.
    """
    bot.send_message(message.chat.id, parse_mode='HTML', text='Сейчас ты увидишь предложение, которое нужно будет '
                                                              'оценить. Нажми <strong>ДА</strong>, '
                                                              'если предложение содержит факт работы, и <strong>НЕТ</strong>, '
                                                              'если не содержит', reply_markup=markup_y_n)
    periphrase_step[message.chat.id] = PERIPHRASE_VERIFY2
    what_to_check = db.get_random_periphrase()
    bot.send_message(message.chat.id, parse_mode='HTML', text=what_to_check)
    # где-то надо прописывать, какой именно факт


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == PERIPHRASE_VERIFY2)
def me_verify_check(message):
    """
    Пользователь вводит свой ответ. Его ответ сравнивается с нашим ответом, и, если ответы совпали, к очкам
    пользователя,     взятым из базы данных, добавляется один и записывается. Еси не совпали, то
    вычитается одно очко соответственно.
    """
    # Проверка на наличие участников
    what_to_check = db.get_check_periphrase() # !!!!!
    # bot.send_message(message.chat.id, parse_mode='HTML', text=what_to_check)
    answer = db.get_periphrase_value(what_to_check)
    if 'ДА' or 'НЕТ' in message.text.split(' '):
        if message.text == answer:
            person_points = db.get_person_points('author')
            person_points += 1
            db.save_person_points(person_points)
            bot.send_message(message.chat.id, 'Спасибо, ответ записан', reply_markup=markup)
            periphrase_step[message.chat.id] = PERIPHRASE_VERIFIED2
        else:
            person_points = db.get_person_points('author')
            person_points -= 1
            db.save_person_points(person_points)
            bot.send_message(message.chat.id, 'Спасибо, ответ записан', reply_markup=markup)
            periphrase_step[message.chat.id] = PERIPHRASE_VERIFIED2
    else:
        bot.send_message(message.chat.id, 'Ты не использовал обязательных участников')


if __name__ == '__main__':
    # bot.set_update_listener(listener)
    bot.polling(none_stop=True)
    while True:
        time.sleep(200)
