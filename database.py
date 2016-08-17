# -*- coding: utf-8 -*-

class DatabaseInteraction:
    """
    Класс взаимодействия с базой данных.
    """

    def connect(self, connection_string):
        """
        Подключиться по connection_string.
        """
        print('Connecting ({}) ...'.format(connection_string))

    def get_fact(self):
        """
        Получить факт из базы данных.
        """
        print('Fact')
        return 'X работает в Y'

    def get_random_periphrase(self):
        """
        Получить рандомный перифраз из базы данных.
        """
        print('Random periphrase')
        return '<strong>ПЕРСОНА</strong> предоставляет услуги по ремонту машин в <strong>ОРГАНИЗАЦИЯ</strong>'

    def get_check_periphrase(self):
        """
        Получить перифраз из базы данных, про который мы точно знаем, содержится там факт или нет.
        """
        print('Check periphrase')
        return '<strong>ПЕРСОНА</strong> работает в <strong>ОРГАНИЗАЦИЯ</strong>'

    def get_periphrase_value(self, fact):
        """
        Получить из базы данных ответ на вопрос, содержится ли в перифразе факт.
        """
        value = 'ДА'
        print(value)
        return value

    def get_points(self, person):
        """
        Получить из базы данных очки пользователя.
        """
        p = 13
        print(p)
        return p

    def save_result(self, result):
        """
        Сохранить в базе данных результат перифраза, предложенный пользователем.
        """
        print('Saving result ({}) ...'.format(result))

    def save_value(self, value):
        """
        Добавить в базу данных оценку пользовтелем наличия факта в перифразе, предложенном другим пользовтелем.
        """
        print('Saving value ({}) ...'.format(value))

    def save_points(self, points):
        """
        Добавить в базу данных очки на доверия пользователю в зависимости от того, правильно или нет он определил
        наличие факта в перифразе.
        """
        print('Saving value ({}) ...'.format(points))

    def disconnect(self):
        """ Отключиться"""
        print('Disconnecting...')

    def __init__(self):
        """ Конструктор"""
        print('Initializing database stub object')