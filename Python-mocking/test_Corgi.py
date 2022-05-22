from unittest.mock import Mock
from unittest import mock
import unittest

import requests
from Corgi import ApiCorgi

class HttpException(Exception):
    pass

class ConnException(Exception):
    pass

class CorgiTestCase(unittest.TestCase):
    def setUp(self):
        self.corgi = ApiCorgi()
    
    @mock.patch("Corgi.requests.get")
    def test_get_connection_error_then_sucess(self, mock_get):
        # Arrange
        mock_response = Mock()
        expected = {
            "breeds": [
                "pembroke",
                "cardigan",
            ]
        }

        # Assign
        mock_response.json.return_value = expected
        conn_error = requests.exceptions.ConnectionError()
        mock_get.side_effect = [conn_error, conn_error, mock_response]
        url = 'http://api.corgidata.com/breeds/'
        response = self.corgi.get(url=url)
        expected_calls = [mock.call(url=url)]* 3

        # Assert
        self.assertEqual(expected_calls, mock_get.call_args_list)
        self.assertEqual(1, mock_response.json.call_count)

        self.assertEqual(response, expected)


    @mock.patch('Corgi.ApiCorgi.handle_http_error')
    @mock.patch('Corgi.requests.get')
    def test_get_http_error(self, mock_get, mock_http_error_handler):
        # Arrange
        mock_response = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_get.return_value = mock_response

        # Assign
        mock_http_error_handler.side_effect = HttpException()
        url = "http://api.corgidata.com/breeds/"
        with self.assertRaises(HttpException):
            self.corgi.get(url=url)

        # Assert
        mock_get.assert_called_once_with(url=url)
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_not_called()
        mock_http_error_handler.assert_called_once_with(http_error)


    @mock.patch('Corgi.ApiCorgi.handle_connection_error')
    @mock.patch('Corgi.requests.get')
    def test_get_connection_error(self, mock_get, mock_conn_error_handler):
        # Arrange
        conn_error = requests.exceptions.ConnectionError()
        mock_get.side_effect = conn_error
        mock_conn_error_handler.side_effect = ConnException()

        # Assign
        url = 'http://api.corgidata.com/breeds/'
        with self.assertRaises(ConnException):
            self.corgi.get(url=url)

        expected_calls = [mock.call(url=url)] * 3

        # Assert
        self.assertEqual(expected_calls, mock_get.call_args_list)
        mock_conn_error_handler.assert_called_once_with(conn_error)    
    
    


if __name__ == "__main__":
    unittest.main()