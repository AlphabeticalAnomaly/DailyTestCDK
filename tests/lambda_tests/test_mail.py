import unittest
from src.mail_client import MailService, MailServiceError
from unittest.mock import Mock


class TestMailService(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.Mail = MailService(client=self.client)

    def test_email_send(self):
        self.Mail.send_email(destination_address="test_address", source_address="test_source", content="test_content")
        self.Mail.client.send_email.assert_called_once_with(Destination={'ToAddresses': ['test_address']}, Message={'Body': {'Text': {'Charset': 'UTF-8', 'Data': 'test_content'}}, 'Subject': {'Charset': 'UTF-8', 'Data': 'Test email'}}, Source='test_source')

    def test_email_exception_handling(self):
        self.Mail = MailService(client=self.client)
        expected_exception = Exception('exception')
        self.Mail.client.send_email.side_effect = expected_exception
        with self.assertRaises(MailServiceError) as context:
            self.Mail.send_email(destination_address="test_address", source_address="test_source", content="test_content")
        self.assertEqual('An error occurred when mail client was called.', context.exception.error)




