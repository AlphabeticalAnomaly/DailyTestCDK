import unittest
from unittest.mock import Mock, patch
from src.lambda_function import read, mail, lambda_handler


class TestHandler(unittest.TestCase):
    @patch('src.lambda_function.read')
    @patch('src.lambda_function.mail')
    def test_calls(self, mock_mail, mock_read):
        event = {"bucket": "test_bucket", "content": "test_content", "address": "test_address"}
        context = Mock()
        handler = lambda_handler(event=event, context=context)
        mock_read.assert_called_with(bucket=event["bucket"], object_key=event["content"])
        object_str = mock_read.return_value
        mock_mail.assert_called_with(source_address=event["address"], destination_address=event["address"], content=object_str)






