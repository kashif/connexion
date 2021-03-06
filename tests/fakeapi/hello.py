#!/usr/bin/env python3

from connexion import problem, request
from connexion import NoContent


def post_greeting(name):
    data = {'greeting': 'Hello {name}'.format(name=name)}
    return data


def post_goodday(name):
    data = {'greeting': 'Hello {name}'.format(name=name)}
    headers = {"Location": "/my/uri"}
    return data, 201, headers


def post_goodday_no_header():
    return {'greeting': 'Hello.'}, 201


def post_goodevening(name):
    data = 'Good evening {name}'.format(name=name)
    headers = {"Location": "/my/uri"}
    return data, 201, headers


def get_list(name):
    data = ['hello', name]
    return data


def get_bye(name):
    return 'Goodbye {name}'.format(name=name), 200


def get_bye_secure(name):
    return 'Goodbye {name} (Secure: {user})'.format(name=name, user=request.user)


def with_problem():
    return problem(type='http://www.example.com/error',
                   title='Some Error',
                   detail='Something went wrong somewhere',
                   status=418,
                   instance='instance1',
                   headers={'x-Test-Header': 'In Test'})


def with_problem_txt():
    return problem(title='Some Error',
                   detail='Something went wrong somewhere',
                   status=418,
                   instance='instance1')


def internal_error():
    return 42 / 0


def get_greetings(name):
    """
    Used to test custom mimetypes
    """
    data = {'greetings': 'Hello {name}'.format(name=name)}
    return data


def multimime():
    return 'Goodbye'


def empty():
    return None, 204


def schema(new_stack):
    return new_stack


def schema_response_object(valid):
    if valid == "invalid_requirements":
        return {"docker_version": 1.0}
    elif valid == "invalid_type":
        return {"image_version": 1.0}
    else:
        return {"image_version": "1.0"}  # valid


def schema_response_string(valid):
    if valid == "valid":
        return "Image version 2.0"
    else:
        return 2.0


def schema_response_integer(valid):
    if valid == "valid":
        return 3
    else:
        return 3.0


def schema_response_number(valid):
    if valid == "valid":
        return 4.0
    else:
        return "Four"


def schema_response_boolean(valid):
    if valid == "valid":
        return True
    else:
        return "yes"


def schema_response_array(valid):
    if valid == "invalid_dict":
        return {
            {"image_version": "1.0"}:
                {"image_version": "2.0"}
        }
    elif valid == "invalid_string":
        return "Not an array."
    else:
        return [
            {"image_version": "1.0"},
            {"image_version": "2.0"}
        ]


def schema_query(image_version=None):
    return {'image_version': image_version}


def schema_list():
    return ''


def schema_format():
    return ''


def test_parameter_validation():
    return ''


def test_required_query_param():
    return ''


def test_no_content_response():
    return NoContent, 204


def test_schema_array(test_array):
    return test_array


def test_schema_int(test_int):
    return test_int
