from requests import post, get
import pytest


def test_teg_post():
    assert post('http://localhost:5000/api/v2/teg', json={'name': "Test"}).json() == {'success': 'OK'}


def test_teg_get():
    assert get('http://localhost:5000/api/v2/teg').json() == {
        'tags': ['python', 'HTML', 'ML_learning', 'bd', 'Author', 'Single', 'Test']}
