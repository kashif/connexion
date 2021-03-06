import flask
import json
import pytest
# we are using "mock" module here for Py 2.7 support
from mock import MagicMock

from connexion.problem import problem
from connexion.decorators.validation import validate_pattern, validate_minimum, validate_maximum, ParameterValidator
from connexion.decorators.validation import validate_min_length
from connexion.decorators.validation import validate_max_length

def test_validate_pattern():
    assert validate_pattern({}, '') is None
    assert validate_pattern({'pattern': 'a'}, 'a') is None
    assert validate_pattern({'pattern': 'a'}, 'b') == 'Invalid value, pattern "a" does not match'


def test_validate_minimum():
    assert validate_minimum({}, 1) is None
    assert validate_minimum({'minimum': 1}, 1) is None
    assert validate_minimum({'minimum': 1.1}, 1) == 'Invalid value, must be at least 1.1'


def test_validate_maximum():
    assert validate_maximum({}, 1) is None
    assert validate_maximum({'maximum': 1}, 1) is None
    assert validate_maximum({'maximum': 0}, 1) == 'Invalid value, must be at most 0'


def test_validate_min_length():
    assert validate_min_length({}, []) is None
    assert validate_min_length({}, [1,]) is None
    assert validate_min_length({"minLength": 1}, [1,]) is None
    assert validate_min_length({"minLength": 2}, [1, 2,]) is None
    assert validate_min_length({"minLength": 3}, [1, 2,]) == 'Length must be at least 3'


def test_validate_max_length():
    assert validate_max_length({}, []) is None
    assert validate_max_length({}, [1,]) is None
    assert validate_max_length({"maxLength": 2}, [1,]) is None
    assert validate_max_length({"maxLength": 2}, [1, 2,]) is None
    assert validate_max_length({"maxLength": 3}, [1, 2, 3, 4]) == 'Length must be at most 3'


def test_parameter_validator(monkeypatch):
    request = MagicMock(name='request')
    request.args = {}
    request.headers = {}
    request.params = {}
    app = MagicMock(name='app')
    app.response_class = lambda a, mimetype, status: json.loads(a)['detail']
    monkeypatch.setattr('flask.request', request)
    monkeypatch.setattr('flask.current_app', app)

    def orig_handler(*args, **kwargs):
        return 'OK'

    params = [{'name': 'p1', 'in': 'path', 'type': 'integer', 'required': True},
              {'name': 'h1', 'in': 'header', 'type': 'string', 'enum': ['a', 'b']},
              {'name': 'q1', 'in': 'query', 'type': 'integer', 'maximum': 3},
              {'name': 'a1', 'in': 'query', 'type': 'array', 'items': {'type': 'integer', 'minimum': 0}}]
    validator = ParameterValidator(params)
    handler = validator(orig_handler)

    assert handler() == "Missing path parameter 'p1'"
    assert handler(p1='123') == 'OK'
    assert handler(p1='') == "Wrong type, expected 'integer' for path parameter 'p1'"
    assert handler(p1='foo') == "Wrong type, expected 'integer' for path parameter 'p1'"
    assert handler(p1='1.2') == "Wrong type, expected 'integer' for path parameter 'p1'"

    request.args = {'q1': '4'}
    assert handler(p1=1) == 'Invalid value, must be at most 3'
    request.args = {'q1': '3'}
    assert handler(p1=1) == 'OK'

    request.args = {'a1': '1,2'}
    assert handler(p1=1) == "OK"
    request.args = {'a1': '1,a'}
    assert handler(p1=1) == "Wrong type, expected 'integer' for query parameter 'a1'"
    request.args = {'a1': '1,-1'}
    assert handler(p1=1) == "Invalid value, must be at least 0"
    del request.args['a1']

    request.headers = {'h1': 'a'}
    assert handler(p1='123') == 'OK'

    request.headers = {'h1': 'x'}
    assert handler(p1='123') == "Enum value must be one of ['a', 'b']"
