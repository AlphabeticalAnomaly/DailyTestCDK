from lambda_function import lambda_handler
import awsgi
import unittest
from unittest.mock import Mock, patch


class TestHandler(unittest.TestCase):

    def setUp(self):
        self.event = Mock()
        self.context = Mock()

    def test_lambda_handler(self):
        awsgi.response = Mock()
        response = lambda_handler(event=self.event, context=self.context)
        assert response == awsgi.response.return_value

    @patch("lambda_function.jsonify")
    def test_lambda_handler_exception(self, mock):
        awsgi.response = Mock()
        awsgi.response.side_effect = Exception
        response = lambda_handler(event=self.event, context=self.context)
        mock.assert_called_with(status=500, message="The server encountered an error.")

