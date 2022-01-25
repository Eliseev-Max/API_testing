import requests
import pytest
import cerberus


req_methods = ['get', 'put', 'patch', 'delete']


def test_status_code_manual_input(base_url, request_method):
    """
    Проверка кода состояния с возможностью
    ввода HTTP-метода через консоль

    """
    resp = request_method(url = 'https://jsonplaceholder.typicode.com/posts/1')
    assert resp.status_code == 200


@pytest.mark.parametrize("method", req_methods)
def test_status_code_auto_input(base_url, method):
    """Проверка кода состояния для всех допускаемых REST-API методов"""
    resp = getattr(requests, method)(url=base_url + '/posts/1')
    assert resp.status_code == 200


def test_api_json_schema(base_url):
    """Проверка структуры ответа за запрос /todos/1"""
    response = requests.get(base_url + "/todos/1")

    schema = {
        "id": {"type": "number"},
        "userId": {"type": "number"},
        "title": {"type": "string"},
        "completed": {"type": "boolean"}
    }

    v = cerberus.Validator()
    assert v.validate(response.json(), schema)


@pytest.mark.parametrize('title, responsed_title',
                         [(-1, '-1'),
                          (0, '0'),
                          ('', ''),
                          (True, "True"),
                          ('#$%','#$%')])
@pytest.mark.parametrize('userId, responsed_userId',
                         [(1, '1'),
                          (2, '2'),
                          (10, '10'),
                          (100,'100')])
def test_api_posr_request(base_url,
                          userId,
                          responsed_userId,
                          title,
                          responsed_title):

    target = base_url + '/posts'
    data = {'userId': userId,
            'source': 'HTML_document',
            'title': title}
    res = requests.post(
        target,
        data=data
    )
    res_json = res.json()

    assert res_json["userId"] == responsed_userId
    assert res_json["source"] == "HTML_document"
    assert res_json["title"] == responsed_title


@pytest.mark.parametrize('userId', [-1, 0, 'a', 11, '#&'])
def test_api_invalid_userId(base_url, userId):
    res = requests.get(
        base_url + "/posts",
        params={'userId': userId}
    )

    assert res.json() == []
