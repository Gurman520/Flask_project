from requests import post, get
import pytest


def test_news_get():
    lis = get('http://localhost:5000/api/v2/news').json()
    assert lis == [{'author': 1, 'author_name': 'Roman', 'data': 'Mon, 06 Jun 2022 00:43:44 GMT', 'id': 1,
                    'text': 'Это первый запуск Проекта, так что БД обновлена!', 'title': 'Старт Проекта!'},
                   {'author': 1, 'author_name': 'Roman', 'data': 'Mon, 06 Jun 2022 00:45:07 GMT', 'id': 2,
                    'text': 'Создали проект', 'title': 'Старт проекта'}]


def test_news_post():
    assert post('http://localhost:5000/api/v2/news',
                json={'title': "Старт проекта", 'author': 1, 'text': "Создали проект"}).json() == {'success': 'OK'}
