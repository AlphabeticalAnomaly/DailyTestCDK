import unittest
from unittest.mock import Mock, patch
from lambda_code.lambda_function import lambda_handler, read


class TestHandler(unittest.TestCase):
    @patch('lambda_code.lambda_function.read')
    @patch('lambda_code.lambda_function.mail')
    def test_calls(self, mock_mail, mock_read):
        event = {"bucket": "test_bucket", "content": "test_content", "address": "test_address"}
        context = Mock()
        handler = lambda_handler(event=event, context=context)
        mock_read.assert_called_with(bucket=event["bucket"], object_key=event["content"])
        object_str = mock_read.return_value
        mock_mail.assert_called_with(source_address=event["address"], destination_address=event["address"], content=object_str)

    def test_fail(self):
        bucket = Mock()
        object_key = Mock()
        reader = read(bucket=bucket, object_key=object_key)
        assert reader == "An error occurred when trying to access the bucket's contents."









