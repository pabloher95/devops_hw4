#from app import app
import pytest
#from unittest.mock import patch

def add(x,y):
    return x + y

def power(x):
    return x**x

def contains(x, y):
    return x in y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

# @pytest.fixture
# def app_tester():
#     app.config["TESTING"] = True
#     with app.test_client() as client:
#         yield client

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_power():
    assert power(2) == 4

def test_contains():
    assert contains('a', 'dad')
    assert not contains('a', 'mom')

def test_multiply():
    assert multiply(2, 3) == 6

def test_subtract():
    assert subtract(3, 4) == 1