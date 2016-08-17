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

# Получить перифраз из базы данных. Получить перефразированный перифраз. Сохранить результат

    def get_random_periphrase(self):
        """
        Получить рандомный перифраз из базы данных.
        """
        print('Random periphrase')
        return '<strong>ПЕРСОНА</strong> предоставляет услуги по ремонту машин в <strong>ОРГАНИЗАЦИЯ</strong>'

    def save_result(self, result):
        """
        Сохранить в базе данных результат перифраза, предложенный пользователем.
        """
        print('Saving result ({}) ...'.format(result))

# Получить рандомный перифраз. Получить очки перифраза. Пересчитать очки перифраза в зависимости от введенной
# пользователем оценки. Внести очки перифраза в базу банных.

    def get_periphrase_points(self, periphrase):
        """
        Добавить в базу данных оценку пользовтелем наличия факта в перифразе, предложенном другим пользовтелем.
        """
        periphrase_points = 47      # Например
        print('Getting periphrase_points  ({}) ...'.format(periphrase_points))
        return periphrase_points

    def save_periphrase_points(self, periphrase_points):
        """
        Добавить в базу данных оценку пользовтелем наличия факта в перифразе, предложенном другим пользовтелем.
        """
        print('Saving periphrase_points ({}) ...'.format(periphrase_points))


# Получить перифраз, про который мы знаем, есть ли в нем факт. Получить оценку перифраза и сравнить в введенными.
# Получить очки человека. Сохранить перекалькулированные очки человека в базу данных.

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
        periphrase_value = 'ДА'                # Например
        print('Getting periphrase_value  ({}) ...'.format(periphrase_value))
        return periphrase_value

    def get_person_points(self, person):
        """
        Получить из базы данных очки пользователя.
        """
        person_points = 13                      # Например
        print('Getting person_points  ({}) ...'.format(person_points))
        return person_points

    def save_person_points(self, person_points):
        """
        Добавить в базу данных очки на доверия пользователю в зависимости от того, правильно или нет он определил
        наличие факта в перифразе.
        """
        print('Saving person_points ({}) ...'.format(person_points))

###############################

    def disconnect(self):
        """ Отключиться"""
        print('Disconnecting...')

    def __init__(self):
        """ Конструктор"""
        print('Initializing database stub object')