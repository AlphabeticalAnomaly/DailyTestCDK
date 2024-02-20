from lambda_function import lambda_handler
import awsgi
import unittest
from unittest.mock import Mock


class TestHandler(unittest.TestCase):

    def setUp(self):
        self.event = Mock()
        self.context = Mock()

    def test_lambda_handler(self):
        awsgi.response = Mock()
        self.handler = lambda_handler(event=self.event, context=self.context)
        assert self.handler == awsgi.response.return_value
