from requests import post, get, delete, put
import pytest


def test_art_list_post():
    assert post('http://localhost:5000//api/v2/list_art', json={'title': "Test",
                                                                'author': 1,
                                                                'text': "./static/article/art_" + str(1) + "_" + str(
                                                                    4) + ".md",
                                                                'tegs': ["python"]}).json() == {'success': 'OK'}


def test_art_list_get():
    assert get('http://localhost:5000//api/v2/list_art').json() == [
        {'author': 1, 'author_name': 'Roman', 'id': 1, 'status': 0, 'tags': ['Single'],
         'text': './static/article/art_1.md', 'title': 'First article'},
        {'author': 1, 'author_name': 'Roman', 'id': 2, 'status': 1, 'tags': ['python'],
         'text': './static/article/art_1_4.md', 'title': 'Test'}]


def test_art_put():
    assert put('http://localhost:5000//api/v2/art/2', json={'title': "Test__1"}).json() == {'success': 'OK'}


def test_art_get():
    assert get('http://localhost:5000//api/v2/art/2').json() == {'author': 1, 'author_name': 'Roman', 'status': 1,
                                                                 'tags': ['python'],
                                                                 'text': './static/article/art_1_4.md',
                                                                 'title': 'Test__1'}


def test_art_delete():
    assert delete('http://localhost:5000//api/v2/art/2').json() == {'success': 'OK'}
