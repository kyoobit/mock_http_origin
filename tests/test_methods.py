import sys
from pathlib import Path

import pytest

from tornado.httpclient import HTTPError
from tornado.testing import AsyncHTTPTestCase

# Append the root directory of this application to system path
sys.path.append(str(Path(__file__).parent.parent))

from app import make_app


## https://www.tornadoweb.org/en/stable/testing.html
class TestRepeaterHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app(debug=True)

    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods

    @pytest.mark.xfail(reason='CONNECT not supported')
    def test_HTTP_method_CONNECT(self):
        response = self.fetch('/', method='CONNECT')

    def test_HTTP_method_DELETE(self):
        response = self.fetch('/', method='DELETE')
        self.assertEqual(response.code, 405)

    def test_HTTP_method_GET(self):
        response = self.fetch('/', method='GET')
        self.assertEqual(response.code, 200)

    def test_HTTP_method_HEAD(self):
        response = self.fetch('/', method='HEAD')
        self.assertEqual(response.code, 200)

    def test_HTTP_method_OPTIONS(self):
        response = self.fetch('/', method='OPTIONS')
        self.assertEqual(response.code, 200)

    def test_HTTP_method_PATCH(self):
        response = self.fetch('/', method='PATCH', body='test')
        self.assertEqual(response.code, 405)

    def test_HTTP_method_POST(self):
        response = self.fetch('/', method='POST', body='test')
        self.assertEqual(response.code, 200)

    def test_HTTP_method_PUT(self):
        response = self.fetch('/', method='PUT', body='test')
        self.assertEqual(response.code, 405)

    @pytest.mark.xfail(reason='TRACE not supported')
    def test_HTTP_method_TRACE(self):
        response = self.fetch('/', method='TRACE')
