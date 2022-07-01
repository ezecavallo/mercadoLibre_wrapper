import os
from unittest import TestCase
from unittest.mock import Mock
from urllib.parse import parse_qs, urlparse

from mercadolibre.client import MercadoLibre
from mercadolibre.response import Response


from mock import call, patch
# from my_module import wrapper_func


requests = Mock()

os.environ.setdefault('client_id', '')
os.environ.setdefault('client_secret', '')
os.environ.setdefault('redirect_url', 'https://localhost:1443/')


class MercadoLibreTests(TestCase):
    def setUp(self):
        self.client_id = os.environ.get('client_id')
        self.client_secret = os.environ.get('client_secret')
        self.site = 'MLA'
        self.client = MercadoLibre(self.client_id, self.client_secret, self.site)
        self.redirect_url = os.environ.get('redirect_url')

    def log_request(self, url):
        # Log a fake request for test output purposes
        print(f'Making a request to {url}')
        print('Request received!')

        # Create a new Mock to imitate a Response
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = {
            'access_token': '',
            'token_type': 'bearer',
            'expires_in': 21600,
            'scope': 'read',
            'user_id': 148262344
        }
        response = Response(response_mock)
        return response

    def test_authorization_url(self):
        url = self.client.authorization_url(self.redirect_url)
        self.assertIsInstance(url, str)
        params = urlparse(url)
        query = parse_qs(params.query)
        self.assertIn('client_id', query)
        self.assertIn(query['client_id'][0], self.client_id)
        self.assertIn('redirect_uri', query)
        self.assertEqual(query['redirect_uri'][0], self.redirect_url)

    def test_authenticate_set_token(self):
        self.client._get_access_token = self.log_request

        response = self.client._set_token(self.client._get_access_token('/oauth/token'))
        data = response.data
        client = self.client

        self.assertIn('access_token', data)
        self.assertEqual(client.access_token,
                         '')

        self.assertIn('expires_in', data)
        self.assertEqual(client.expires_in, 21600)

        self.assertIn('user_id', data)
        self.assertEqual(client.user_id, 148262344)

    @patch.object(MercadoLibre, '_get_access_token')
    def test_get_access_token(self, mocked_api_func):

        # response = wrapper_func('user', 'pass')
        response = self.client._get_access_token(self.redirect_url)
        self.assertTrue(mocked_api_func.called)
        self.assertEqual(
            mocked_api_func.call_args_list,
            [call(self.redirect_url)]
        )

        self.assertEqual(mocked_api_func.return_value, response)
