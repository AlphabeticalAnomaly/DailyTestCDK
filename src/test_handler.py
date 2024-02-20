from unittest.mock import Mock
import json
import unittest
from app_task import send_email
from datetime import datetime


class TestHandler(unittest.TestCase):

    def test_send_email(self):
        current_date = datetime.today().strftime('%Y.%m.%d.%H.%M.%S')
        dict = {"bucket": "test_bucket", "content": "test_content", "address": "test_address"}
        reader = Mock()
        mailer = Mock()
        dynamo = Mock()
        send_email(data=dict, reader=reader, mailer=mailer, dynamo=dynamo)
        reader.read_object_content.assert_called_with(bucket="test_bucket", object_key="test_content")
        mailer.send_email.assert_called_with(source_address="test_address", destination_address="test_address", content=reader.read_object_content.return_value)
        dynamo.dynamo_put_item.assert_called_with(item={"email": "test_address", "date": current_date, "content": "test_content"})
