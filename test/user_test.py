from requests import post, get, delete, put
import pytest


def test_user_get():
    lis = get('http://localhost:5000//api/v2/user/1').json()
    assert lis == {'access': 0, 'country': 'Russian', 'email': 'Roman.Python.test@gmail.com',
                   'git': 'https://github.com/Gurman520', 'id': 1, 'name': 'Roman', 'sex': 'man',
                   'surname': 'Sulima',
                   'vk': 'http://vk.com/furman521'}


def test_user_put():
    assert put('http://localhost:5000//api/v2/user/1', json={'f_name': 'Romanidzs'}).json() == {'success': 'OK'}


def test_user_list_get():
    lis = get('http://localhost:5000//api/v2/list_user').json()
    assert lis == [
        {'country': 'Russian', 'email': 'Roman.Python.test@gmail.com', 'id': 1, 'level': 0, 'name': 'Romanidzs',
         'sex': 'man', 'surname': 'Sulima'}]


def test_user_put2():
    assert put('http://localhost:5000//api/v2/user/1', json={'f_name': 'Roman'}).json() == {'success': 'OK'}
