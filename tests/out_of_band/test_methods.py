import logging

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


## https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
HTTP_METHOD_TESTS = [
    ({'method': 'CONNECT', 'xfail': 'method not implemented in HTTP client'}, None),
    ({'method': 'DELETE'}, {'code': 405}),
    ({'method': 'GET'}, {'code': 200}),
    ({'method': 'HEAD'}, {'code': 200}),
    ({'method': 'OPTIONS'}, {'code': 200}),
    ({'method': 'PATCH', 'body': 'test'}, {'code': 405}),
    ({'method': 'POST', 'body': 'test'}, {'code': 200}),
    ({'method': 'PUT', 'body': 'test'}, {'code': 405}),
    ({'method': 'TRACE', 'xfail': 'method not implemented in HTTP client'}, None),
    ]


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', HTTP_METHOD_TESTS,
    ids=[test[0]['method'] for test in HTTP_METHOD_TESTS])
def test_HTTP_METHOD(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/ping", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    if req['method'] in ['GET', 'HEAD']:
        assert int(response.headers.get('Content-Length')) == 25 # gzip
        assert response.headers.get('Content-Type') == 'text/plain'
        assert response.headers.get('Etag') is not None
    elif req['method'] == 'OPTIONS':
        assert response.headers.get('Access-Control-Allow-Origin') == '*'
        assert response.headers.get('Access-Control-Allow-Methods') == 'GET,HEAD,OPTIONS'
        assert response.headers.get('Access-Control-Allow-Headers') == 'Origin,Range'
        assert response.headers.get('Access-Control-Expose-Headers') == 'Cache-Control,Date,Expires,Server'
        assert response.headers.get('Access-Control-Max-Age') == '60'

    ## Check response body for expected values
    if req['method'] in ['GET', 'POST']:
        assert response.body == b'pong\n'
    else:
        assert response.body == b''
