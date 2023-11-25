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


BOILERPLATE_TESTS = [
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


## -----------------------------------------------------------------------------


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_without_parameters(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/without/parameters.ext", **req)

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
        assert response.body.decode().find(f"> {req['method']} /test/without/parameters.ext HTTP/1.1") != -1
        if req['method'] == 'POST':
            assert response.body.decode().find("* POST DATA b'test'") != -1


## -----------------------------------------------------------------------------


@pytest.mark.skip('Not implemented yet')
def test_with_Transfer_Encoding_chunked(address):
    """
  When "content" is combined with a "Transfer-Encoding: chunked" response header 
  the response body content will be formatted into a chunked response.
  (Use --raw with curl to view chunked content)
    ?header=transfer-encoding:chunked&content=<int>[&fill=<str>][&chunk_length=<int>][&no_end_of_content=<str>]

    chunk_length=<int> (default: 64) controls the length of each chunk in the 
      response generated.

    no_end_of_content=<str> the presence of this attribute will suppress the 
      end of content lines ('0\r\n\r\n') in the chunked response. The HTTP 
      client will likely hang waiting on the expected end of content lines.
    """
    raise NotImplementedError('...work to do')


## -----------------------------------------------------------------------------


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_content_no_value(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?content", **req)

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
        assert response.body.decode().find(f"> {req['method']} /test/with.ext?content HTTP/1.1") != -1
        if req['method'] == 'POST':
            assert response.body.decode().find("* POST DATA b'test'") != -1


## -----------------------------------------------------------------------------


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_content(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?content=1024", **req)

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
        assert len(response.body) == 1024


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_content_encoding_identity(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?content=1024&encoding=identity", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert int(response.headers.get('Content-Length')) == 1024
    assert response.headers.get('Content-Type') == 'text/plain'
    if req['method'] != 'HEAD':
        assert int(response.headers.get('Content-Length')) > 0

    ## Check response body for expected values
    if req['method'] != 'HEAD':
        assert len(response.body) == 1024


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_content_encoding_gzip(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?content=1024&encoding=gzip", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert int(response.headers.get('Content-Length')) < 1024
    assert response.headers.get('Content-Type') == 'text/plain'
    if req['method'] != 'HEAD':
        assert int(response.headers.get('Content-Length')) > 0

    ## Check response body for expected values
    if req['method'] != 'HEAD':
        ## HTTP client will decompress with compress options enabled
        if response.headers.get('X-Consumed-Content-Encoding', False):
            assert len(response.body) == 1024
        else:
            assert len(response.body) < 1024


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_content_fill(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?content=1024&fill=aaaa", **req)

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
        assert len(response.body) == 1024
        assert response.body.decode().startswith('aaaaaaaaaaaaaaaaaa') is True


@pytest.mark.skip('Not implemented yet')
def test_with_content_fill_lipsum(caplog, address):
    raise NotImplementedError('...work to do')


@pytest.mark.skip('Not implemented yet')
def test_with_content_fill_ascii(caplog, address):
    raise NotImplementedError('...work to do')


## -----------------------------------------------------------------------------


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_debug(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?debug", **req)

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
        assert response.body.decode().startswith('# DEBUG: request.arguments') is True
        assert response.body.decode().find(f"{req['method']} /test/with.ext?debug HTTP/1.1") != -1


## -----------------------------------------------------------------------------


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_delay(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?delay=0.25", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    if req['method'] != 'HEAD':
        assert int(response.headers.get('Content-Length')) > 0
    assert response.headers.get('X-Delay') == '0.25 set by query string'

    ## Check response body for expected values
    if req['method'] != 'HEAD':
        assert response.body.decode().find(f"{req['method']} /test/with.ext?delay=0.25 HTTP/1.1") != -1
        assert response.body.decode().find('< X-Delay: 0.25 set by query string') != -1


## -----------------------------------------------------------------------------


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_header_add(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?header=x-wr-test:Test", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    if req['method'] != 'HEAD':
        assert int(response.headers.get('Content-Length')) > 0
    assert response.headers.get('X-Wr-Test') == 'Test'

    ## Check response body for expected values
    if req['method'] != 'HEAD':
        assert response.body.decode().find(f"{req['method']} /test/with.ext?header=x-wr-test:Test HTTP/1.1") != -1
        assert response.body.decode().find('< X-Wr-Test: Test') != -1


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_header_modify(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?header=server:Test", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server') == 'Test'
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    if req['method'] != 'HEAD':
        assert int(response.headers.get('Content-Length')) > 0

    ## Check response body for expected values
    if req['method'] != 'HEAD':
        assert response.body.decode().find(f"{req['method']} /test/with.ext?header=server:Test HTTP/1.1") != -1
        assert response.body.decode().find('< Server: Test') != -1


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_header_remove(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?header=Content-Type:", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') is None
    if req['method'] != 'HEAD':
        assert int(response.headers.get('Content-Length')) > 0

    ## Check response body for expected values
    if req['method'] != 'HEAD':
        assert response.body.decode().find(f"{req['method']} /test/with.ext?header=Content-Type: HTTP/1.1") != -1
        assert response.body.decode().find('< Content-Type:') == -1


## -----------------------------------------------------------------------------


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_quite(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?quiet", **req)

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
        assert response.body.decode().startswith(f"> {req['method']} /test/with.ext?quiet HTTP/1.1") is True
        assert response.body.decode().endswith('<\n') is True


## -----------------------------------------------------------------------------


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_set_addr_match(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    req['headers']['Forwarded'] = f"for={address.split(':',1)[0]}"

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?set=delay:0.25,status:599,addr:{address.split(':',1)[0]}", **req)

    ## Check response code for the expected value
    assert response.code == 599

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    assert int(response.headers.get('Content-Length')) == 0
    assert response.headers.get('X-Delay') == '0.25 set by query string'
    assert response.headers.get('X-Status-Code') == '599 set by query string'


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_set_addr_not_matched(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?set=delay:0.25,status:599,addr:4.3.2.1", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    assert int(response.headers.get('Content-Length')) > 0
    assert response.headers.get('X-Delay') is None
    assert response.headers.get('X-Status-Code') is None


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_set_addr_match_proxied(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    req['headers']['Forwarded'] = 'for=4.3.2.1'

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?set=delay:0.25,status:599,addr:4.3.2.1", **req)

    ## Check response code for the expected value
    assert response.code == 599

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    assert int(response.headers.get('Content-Length')) == 0
    assert response.headers.get('X-Delay') == '0.25 set by query string'
    assert response.headers.get('X-Status-Code') == '599 set by query string'


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_set_addr_not_matched_proxied(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    req['headers']['Forwarded'] = 'for=8.7.6.5'

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?set=delay:0.25,status:599,addr:4.3.2.1", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    assert int(response.headers.get('Content-Length')) > 0
    assert response.headers.get('X-Delay') is None
    assert response.headers.get('X-Status-Code') is None


## -----------------------------------------------------------------------------


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_set_header_match(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    req['headers']['Host'] = 'Test'

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?set=delay:0.25,status:599,host:test", **req)

    ## Check response code for the expected value
    assert response.code == 599

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    assert int(response.headers.get('Content-Length')) == 0
    assert response.headers.get('X-Delay') == '0.25 set by query string'
    assert response.headers.get('X-Status-Code') == '599 set by query string'


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_set_header_not_matched(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    req['headers']['Host'] = 'Another-Test'

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?set=delay:0.25,status:599,host:test", **req)

    ## Check response code for the expected value
    assert response.code == expected['code']

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    assert int(response.headers.get('Content-Length')) > 0
    assert response.headers.get('X-Delay') is None
    assert response.headers.get('X-Status-Code') is None


## -----------------------------------------------------------------------------


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_status(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?status=418", **req)

    ## Check response code for the expected value
    assert response.code == 418

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    assert int(response.headers.get('Content-Length')) == 0
    assert response.headers.get('X-Status-Code') == '418 set by query string'


## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
## Use the `method' as the test name id
@pytest.mark.parametrize('req, expected', BOILERPLATE_TESTS,
    ids=[test[0]['method'] for test in BOILERPLATE_TESTS])
def test_with_status(caplog, address, req, expected):
    caplog.set_level(logging.DEBUG)
    print(f"req: {req!r}")
    print(f"expected: {expected!r}")

    ## Catch expected failures
    if req.get('xfail', False):
        pytest.xfail(req['xfail'])

    ## Make the HTTP request
    response = fetch(f"http://{address}/test/with.ext?status=672&reason=Special+Weirdness", **req)

    ## Check response code for the expected value
    assert response.code == 672
    assert response.reason == 'Special Weirdness'

    ## Check response headers for expected values
    assert response.headers.get('Server').startswith('Python/Tornado/Mock_HTTP_Origin')
    assert response.headers.get('Cache-Control') == 'private, no-store'
    assert response.headers.get('Content-Type') == 'text/plain'
    assert int(response.headers.get('Content-Length')) == 0
    assert response.headers.get('X-Status-Code') == '672 set by query string'
