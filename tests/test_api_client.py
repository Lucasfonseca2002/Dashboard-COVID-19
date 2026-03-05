import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import requests
import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.api_client import COVID19APIClient

class TestCOVID19APIClient(unittest.TestCase):

    def setUp(self):
        self.client = COVID19APIClient()
        self.client.max_retries = 1 # Para testes mais rápidos

    @patch('src.data.api_client.requests.get')
    def test_make_request_success(self, mock_get):
        # Mocking a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.client._make_request("http://test.url")
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch('src.data.api_client.requests.get')
    def test_make_request_timeout(self, mock_get):
        # Mocking a timeout exception
        mock_get.side_effect = requests.exceptions.Timeout

        response = self.client._make_request("http://test.url")
        self.assertIsNone(response)

    @patch('src.data.api_client.requests.get')
    def test_get_brasil_data_empty_results(self, mock_get):
        # Mocking empty results
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': []}
        mock_get.return_value = mock_response

        df = self.client.get_brasil_data()
        self.assertIsNone(df)

    @patch('src.data.api_client.requests.get')
    def test_get_world_top_countries(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'country': 'USA', 'cases': 100},
            {'country': 'Brazil', 'cases': 90},
            {'country': 'India', 'cases': 80}
        ]
        mock_get.return_value = mock_response

        df = self.client.get_world_top_countries()
        self.assertIsNotNone(df)
        self.assertNotIn('Brazil', df['country'].values)
        self.assertEqual(len(df), 2)

if __name__ == '__main__':
    unittest.main()
