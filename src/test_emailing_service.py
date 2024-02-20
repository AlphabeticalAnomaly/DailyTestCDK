from unittest.mock import Mock
import unittest
from emailing_service import EmailingService
from datetime import datetime


class TestEmailingService(unittest.TestCase):
    def setUp(self):
        self.data = {"bucket": "test_bucket", "content": "test_content", "address": "test_address"}
        self.current_date = datetime.today().strftime('%Y.%m.%d.%H.%M.%S')
        self.reader = Mock()
        self.mailer = Mock()
        self.dynamo = Mock()
        self.email_service = EmailingService(reader=self.reader, mailer=self.mailer, dynamo=self.dynamo)

    def test_send_email(self):

        self.email_service.send_email(bucket=self.data["bucket"], address=self.data["address"], content=self.data["content"])
        self.email_service.reader.read_object_content.assert_called_with(bucket="test_bucket", object_key="test_content")
        self.email_service.dynamo.dynamo_put_item.assert_called_with(item={"email": "test_address",
                                                                           "date": self.current_date,
                                                                           "content": "test_content"
                                                                           })
        self.email_service.mailer.send_email.assert_called_with(source_address="test_address",
                                                                destination_address="test_address",
                                                                content=self.email_service.reader.read_object_content.return_value)


