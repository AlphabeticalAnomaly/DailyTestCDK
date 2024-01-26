import unittest
from unittest.mock import Mock
from lambda_function import lambda_handler


class TestHandler(unittest.TestCase):
    def test_handler(self):
        event = {"bucket": "test_bucket", "content": "test_content", "address": "test_address"}
        context = Mock()
        reader = Mock()
        mailer = Mock()
        handler = lambda_handler(event=event, context=context, reader=reader, mailer=mailer)
        reader.read_object_content.assert_called_with(bucket=event["bucket"], object_key=event["content"])
        mailer.send_email.assert_called_with(source_address=event["address"], destination_address=event["address"], content=reader.read_object_content.return_value)



