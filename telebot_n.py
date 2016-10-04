# -*- coding: utf-8 -*-

import random

import pymorphy2
import telebot
from telebot import types

import config
from database import DatabaseInteraction

bot = telebot.TeleBot(config.token)
db = DatabaseInteraction()
morph = pymorphy2.MorphAnalyzer()

# Создание кастомной клавиатуры
markup = types.ReplyKeyboardMarkup()
markup.row('/create', '/verify', '/verify2')
markup.row('/start', '/help')

markup_y_n = types.ReplyKeyboardMarkup()
markup_y_n.row('Да', 'Нет')

markup_help = types.ReplyKeyboardMarkup()
markup_help.row('Помочь', 'Занят')

PERIPHRASE_CREATE = 'create'
PERIPHRASE_CREATED = 'created'
PERIPHRASE_VERIFY = 'verify'
PERIPHRASE_VERIFIED = 'verified'
PERIPHRASE_VERIFY2 = 'verify2'
PERIPHRASE_VERIFIED2 = 'verified2'
WILL_YOU_HELP_CREATE = 'will_you_help_create'
WILL_YOU_HELP_CHECK = 'will_you_help_сheck'
WILL_YOU_HELP_VERIFY = 'will_you_help_verify'
BUSY = 'busy'

periphrase_step = {}

with open('data/hello.txt', 'r', encoding='utf-8') as hello:
    hello = hello.readlines()

with open('data/help.txt', 'r', encoding='utf-8') as help:
    help = help.readlines()

with open('data/create.txt', 'r', encoding='utf-8') as ccreate:
    ccreate = ccreate.readlines()

with open('data/verify.txt', 'r', encoding='utf-8') as vverify:
    vverify = vverify.readlines()

with open('data/check.txt', 'r', encoding='utf-8') as ccheck:
    ccheck = ccheck.readlines()

with open('data/thanks.txt', 'r', encoding='utf-8') as thanks:
    thanks = thanks.readlines()

with open('data/sorry.txt', 'r', encoding='utf-8') as sorry:
    sorry = sorry.readlines()


@bot.message_handler(commands=['start'])
def send_message(message):
    """
    Приветственное сообщение.
    """
    bot.send_message(message.chat.id, random.choice(hello), reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_message(message):
    """
    Приветственное сообщение.
    """
    bot.send_message(message.chat.id, random.choice(help), reply_markup=markup)


@bot.message_handler(commands=['create'])
def create(message):
    """
    При выборе команды create пользователь получает рандомный перифраз.
    """
    bot.send_message(message.chat.id, str(random.choice(ccreate)), reply_markup=markup_help)
    periphrase_step[message.chat.id] = WILL_YOU_HELP_CREATE


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == WILL_YOU_HELP_CREATE)
def will_you_help_create(message):
    if 'Помочь' in message.text.split(' '):
        bot.send_message(message.chat.id, parse_mode='HTML', text=db.get_random_periphrase())
        keyboard_hider = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, 'Как это сказать иначе?', reply_markup=keyboard_hider)
        periphrase_step[message.chat.id] = PERIPHRASE_CREATE
    if 'Занят' in message.text.split(' '):
        bot.send_message(message.chat.id, str(random.choice(sorry)), reply_markup=markup)
        periphrase_step[message.chat.id] = BUSY


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == PERIPHRASE_CREATE)
def me_create(message):
    """
    Пользователь вводит перифраз, который потом записывается в базу данных.
    """

    # Проверка на наличие участников
    # if morph.parse('Вася')[0].normal_form and morph.parse('ABBYY')[0].normal_form in message.text.split(' '): # Лемматизирую не то, что нужно
    if 'вася' and 'abbyy' in [morph.parse(w)[0].normal_form for w in message.text.split(' ')]:
        db.save_result(message.text)
        # keyboard_hider = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, random.choice(thanks), reply_markup=markup)
        periphrase_step[message.chat.id] = PERIPHRASE_CREATED
    else:
        bot.send_message(message.chat.id, 'Ты не использовал обязательных участников')
    # Добавить проверку на оригинальность


@bot.message_handler(commands=['verify'])
def verify(message):
    """
    Верификация перифразов, предложенных другими пользователями. Нужно на кнопках выбрать да или нет.
    """
    bot.send_message(message.chat.id, str(random.choice(vverify)), reply_markup=markup_help)
    periphrase_step[message.chat.id] = WILL_YOU_HELP_VERIFY
    # где-то надо прописывать, какой именно факт


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == WILL_YOU_HELP_VERIFY)
def will_you_help_verify(message):
    if 'Помочь' in message.text.split(' '):
        what_to_check = db.get_random_periphrase()
        bot.send_message(message.chat.id, parse_mode='HTML', text=db.get_random_periphrase(), reply_markup=markup_y_n)
        bot.send_message(message.chat.id, parse_mode='HTML', text=db.get_random_periphrase())
        # bot.send_message(message.chat.id, parse_mode='HTML', text=db.get_random_periphrase())
        # keyboard_hider = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, 'Эти предложения об одном и том же?', reply_markup=markup_y_n)
        periphrase_step[message.chat.id] = PERIPHRASE_VERIFY
    if 'Занят' in message.text.split(' '):
        bot.send_message(message.chat.id, str(random.choice(sorry)), reply_markup=markup)
        periphrase_step[message.chat.id] = BUSY


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == PERIPHRASE_VERIFY)
def me_verify(message):
    """
    Пользователь вводит ответ, который потом записывается в базу данных.
    """
    what_to_check = db.get_random_periphrase()  # !!!!!
    # bot.send_message(message.chat.id, parse_mode='HTML', text=what_to_check)
    # Проверка на наличие участников
    if 'Да' in message.text.split(' '):
        periphrase_points = db.get_periphrase_points(what_to_check)
        periphrase_points += 1
        db.save_periphrase_points(periphrase_points)
        bot.send_message(message.chat.id, random.choice(thanks), reply_markup=markup)
        periphrase_step[message.chat.id] = PERIPHRASE_VERIFIED
    elif 'Нет' in message.text.split(' '):
        periphrase_points = db.get_periphrase_points(what_to_check)
        periphrase_points -= 1
        db.save_periphrase_points(periphrase_points)
        # keyboard_hider = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, random.choice(thanks), reply_markup=markup)
        periphrase_step[message.chat.id] = PERIPHRASE_VERIFIED
    else:
        bot.send_message(message.chat.id, 'Ты не использовал обязательных участников')


@bot.message_handler(commands=['verify2'])
def verify_check(message):
    """
    Верификация перифразов, про которые мы точно знаем, содержится в них факт или нет. Нужно для проверки пользователя
    'на вшивость'.
    """
    bot.send_message(message.chat.id, random.choice(ccheck), reply_markup=markup_help)
    periphrase_step[message.chat.id] = WILL_YOU_HELP_CHECK
    # где-то надо прописывать, какой именно факт


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == WILL_YOU_HELP_CHECK)
def will_you_help_check(message):
    if 'Помочь' in message.text.split(' '):
        bot.send_message(message.chat.id, parse_mode='HTML', text=db.get_random_periphrase(), reply_markup=markup_y_n)
        bot.send_message(message.chat.id, 'Здесь есть факт работы?')
        periphrase_step[message.chat.id] = PERIPHRASE_VERIFY2
    if 'Занят' in message.text.split(' '):
        bot.send_message(message.chat.id, str(random.choice(sorry)), reply_markup=markup)
        periphrase_step[message.chat.id] = BUSY


@bot.message_handler(func=lambda message: periphrase_step.get(message.chat.id) == PERIPHRASE_VERIFY2)
def me_verify_check(message):
    """
    Пользователь вводит свой ответ. Его ответ сравнивается с нашим ответом, и, если ответы совпали, к очкам
    пользователя,     взятым из базы данных, добавляется один и записывается. Еси не совпали, то
    вычитается одно очко соответственно.
    """
    # Проверка на наличие участников
    what_to_check = db.get_check_periphrase()
    answer = db.get_periphrase_value(what_to_check)
    if 'Да' or 'Нет' in message.text.split(' '):
        if message.text == answer:
            person_points = db.get_person_points('author')
            person_points += 1
            db.save_person_points(person_points)
            bot.send_message(message.chat.id, random.choice(thanks), reply_markup=markup)
            periphrase_step[message.chat.id] = PERIPHRASE_VERIFIED2
        else:
            person_points = db.get_person_points('author')
            person_points -= 1
            db.save_person_points(person_points)
            bot.send_message(message.chat.id, random.choice(thanks), reply_markup=markup)
            periphrase_step[message.chat.id] = PERIPHRASE_VERIFIED2
    else:
        bot.send_message(message.chat.id, 'Ты не использовал обязательных участников')


if __name__ == '__main__':
    # bot.set_update_listener(listener)
    bot.polling(none_stop=True)
    while True:
        time.sleep(200)

# В help описать понятия: факт работы, обязательно использовать участников. Задай свой вопрос
# у васи, васе
