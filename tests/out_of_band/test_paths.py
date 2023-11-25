import logging
import json

## python -m pip install --upgrade pip pytest
import pytest

## python -m pip install --upgrade pip tornado
from tornado import httpclient


## -----------------------------------------------------------------------------


def fetch(url:str, **kwargs):
    """HTTP Client
    See Also:
      * https://www.tornadoweb.org/en/stable/httpclient.html#http-client-interfaces
    """
    response = None
    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch(url, **kwargs)
    except httpclient.HTTPError as err:
        response = err.response
    except Exception as err:
        response = err
    finally:
        http_client.close()
        print(f"response {type(response)}: {response!r}")
        if hasattr(response, 'request'):
            print(f"request: {response.request!r}")
            print(f"request.headers: {[h for h in response.request.headers.get_all()]!r}")
        if hasattr(response, 'code'):
            print(f"response.code: {response.code!r}")
            print(f"response.headers: {[h for h in response.headers.get_all()]!r}")
            print(f"response.body: {response.body!r}")
        return response


## -----------------------------------------------------------------------------


FOOTBALL_TESTS = [
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'Content-Length': 1384, 'Content-Type': 'image/svg+xml', 'body_length': 1384}),
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'Content-Length': 795, 'Content-Type': 'image/svg+xml', 'body_length': 1384}),

    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'Content-Length': 1384, 'Content-Type': 'image/svg+xml', 'body_length': 0}),
    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'Content-Length': 795, 'Content-Type': 'image/svg+xml', 'body_length': 0}),

    ({'method': 'OPTIONS', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'Content-Length': 0, 'Content-Type': 'text/plain', 'body_length': 0}),
    ({'method': 'OPTIONS', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'Content-Length': 0, 'Content-Type': 'text/plain', 'body_length': 0}),

    ({'method': 'POST', 'headers': {'Accept-Encoding': 'identity'}, 'body': 'test', 'decompress_response': False},
        {'code': 200, 'Content-Length': 1384, 'Content-Type': 'image/svg+xml', 'body_length': 1384}),
    ({'method': 'POST', 'headers': {'Accept-Encoding': 'gzip'}, 'body': 'test'},
        {'code': 200, 'Content-Length': 795, 'Content-Type': 'image/svg+xml', 'body_length': 1384}),
    ]


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', FOOTBALL_TESTS,
    ids=[test[0]['method'] for test in FOOTBALL_TESTS])
def test_football(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/football.svg", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == expected['Content-Type']
    assert int(response.headers.get('Content-Length')) == expected['Content-Length']

    ## Check response body for expected values
    assert len(response.body) == expected['body_length']


## -----------------------------------------------------------------------------


HELP_TESTS = [
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'body_length': 5460}),
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'body_length': 5505}),

    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'body_length': 0}),
    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'body_length': 0}),

    ({'method': 'OPTIONS', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'body_length': 0}),
    ({'method': 'OPTIONS', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'body_length': 0}),

    ({'method': 'POST', 'headers': {'Accept-Encoding': 'identity'}, 'body': 'test', 'decompress_response': False},
        {'code': 200, 'body_length': 5552}),
    ({'method': 'POST', 'headers': {'Accept-Encoding': 'gzip'}, 'body': 'test'},
        {'code': 200, 'body_length': 5597}),
    ]


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', HELP_TESTS,
    ids=[test[0]['method'] for test in HELP_TESTS])
def test_help(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/help", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    if expected['body_length'] > 0:
        assert int(response.headers.get('Content-Length')) > 0

    ## Check response body for expected values
    ## Proxied requests may include additional headers causing the body
    ## length to increase from a direct test of the Tornado server
    assert len(response.body) >= expected['body_length']
    if expected['body_length'] > 0:
        assert response.body.decode().startswith('# Hello World!') is True


## -----------------------------------------------------------------------------


PING_TESTS = [
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'body_length': 5}),
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'body_length': 5}),

    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'body_length': 0}),
    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'body_length': 0}),

    ({'method': 'OPTIONS', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'body_length': 0}),
    ({'method': 'OPTIONS', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'body_length': 0}),

    ({'method': 'POST', 'headers': {'Accept-Encoding': 'identity'}, 'body': 'test', 'decompress_response': False},
        {'code': 200, 'body_length': 5}),
    ({'method': 'POST', 'headers': {'Accept-Encoding': 'gzip'}, 'body': 'test'},
        {'code': 200, 'body_length': 5}),
    ]


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', PING_TESTS,
    ids=[test[0]['method'] for test in PING_TESTS])
def test_ping(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/ping", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    if expected['body_length'] > 0:
        assert int(response.headers.get('Content-Length')) > 0

    ## Check response body for expected values
    assert len(response.body) == expected['body_length']
    if expected['body_length'] > 0:
        assert response.body == b'pong\n'


## -----------------------------------------------------------------------------


HELLO_WORLD_TESTS = [
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'body_length': 14}),
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'body_length': 14}),

    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'body_length': 0}),
    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'body_length': 0}),

    ({'method': 'OPTIONS', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200, 'body_length': 0}),
    ({'method': 'OPTIONS', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200, 'body_length': 0}),

    ({'method': 'POST', 'headers': {'Accept-Encoding': 'identity'}, 'body': 'test', 'decompress_response': False},
        {'code': 200, 'body_length': 14}),
    ({'method': 'POST', 'headers': {'Accept-Encoding': 'gzip'}, 'body': 'test'},
        {'code': 200, 'body_length': 14}),
    ]


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', HELLO_WORLD_TESTS,
    ids=[test[0]['method'] for test in HELLO_WORLD_TESTS])
def test_hello_world(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/hello_world", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    if expected['body_length'] > 0:
        assert int(response.headers.get('Content-Length')) > 0

    ## Check response body for expected values
    assert len(response.body) == expected['body_length']
    if expected['body_length'] > 0:
        assert response.body == b'Hello, World!\n'


## -----------------------------------------------------------------------------


ENDSWITH_JSON_TESTS = [
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200}),
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200}),

    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200}),
    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200}),

    ({'method': 'POST', 'headers': {'Accept-Encoding': 'identity'}, 'body': 'test', 'decompress_response': False},
        {'code': 200}),
    ({'method': 'POST', 'headers': {'Accept-Encoding': 'gzip'}, 'body': 'test'},
        {'code': 200}),
    ]


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', ENDSWITH_JSON_TESTS,
    ids=[test[0]['method'] for test in ENDSWITH_JSON_TESTS])
def test_endswith_json(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/ends/with.json", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/json'
    if req['method'] != 'HEAD':
        assert int(response.headers.get('Content-Length')) > 0

    ## Check response body for expected values
    if req['method'] != 'HEAD':
        assert len(response.body) > 0
        body = json.loads(response.body.decode())
        assert body['request']['path'] == '/test/ends/with.json'
        assert body['response']['status_code'] == 200
        assert ['Content-Type', 'text/json'] in body['response']['headers']


## -----------------------------------------------------------------------------


ACCEPT_JSON_TESTS = [
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'identity', 'Accept': 'text/json'},
        'decompress_response': False}, {'code': 200}),
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'gzip', 'Accept': 'text/json'}},
        {'code': 200}),

    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'identity', 'Accept': 'text/json'},
        'decompress_response': False}, {'code': 200}),
    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'gzip', 'Accept': 'text/json'}},
        {'code': 200}),

    ({'method': 'POST', 'headers': {'Accept-Encoding': 'identity', 'Accept': 'text/json'},
        'body': 'test', 'decompress_response': False}, {'code': 200}),
    ({'method': 'POST', 'headers': {'Accept-Encoding': 'gzip', 'Accept': 'text/json'}, 'body': 'test'},
        {'code': 200}),
    ]


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', ACCEPT_JSON_TESTS,
    ids=[test[0]['method'] for test in ACCEPT_JSON_TESTS])
def test_accept_json(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/accept/json.ext", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/json'
    if req['method'] != 'HEAD':
        assert int(response.headers.get('Content-Length')) > 0

    ## Check response body for expected values
    if req['method'] != 'HEAD':
        assert len(response.body) > 0
        body = json.loads(response.body.decode())
        assert body['request']['path'] == '/test/accept/json.ext'
        assert body['response']['status_code'] == 200
        assert ['Content-Type', 'text/json'] in body['response']['headers']


## -----------------------------------------------------------------------------


DEFAULT_TESTS = [
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200}),
    ({'method': 'GET', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200}),

    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'identity'}, 'decompress_response': False},
        {'code': 200}),
    ({'method': 'HEAD', 'headers': {'Accept-Encoding': 'gzip'}},
        {'code': 200}),

    ({'method': 'POST', 'headers': {'Accept-Encoding': 'identity'}, 'body': 'test', 'decompress_response': False},
        {'code': 200}),
    ({'method': 'POST', 'headers': {'Accept-Encoding': 'gzip'}, 'body': 'test'},
        {'code': 200}),
    ]


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', DEFAULT_TESTS,
    ids=[test[0]['method'] for test in DEFAULT_TESTS])
def test_default(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/default/file.ext", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    if req['method'] != 'HEAD':
        assert int(response.headers.get('Content-Length')) > 0

    ## Check response body for expected values
    if req['method'] != 'HEAD':
        assert len(response.body) > 0
        assert response.body.decode().startswith('# Hello World!') is False
        assert response.body.decode().find(f"> {req['method']} /test/default/file.ext HTTP/1.1") != -1
        if req['method'] == 'POST':
            assert response.body.decode().find("* POST DATA b'test'") != -1
