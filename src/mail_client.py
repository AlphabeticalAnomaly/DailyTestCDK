from abc import ABC, abstractmethod
import boto3.session
import boto3


class MailServiceError(Exception):
    def __init__(self, message, cause):
        self.message = message
        self.cause = cause


class IMailService(ABC):

    @abstractmethod
    def send_email(self, source_address=str, destination_address=str, content=str):
        pass


class MailService(IMailService):

    def __init__(self, client=boto3.client('ses', 'eu-north-1')):
        self.client = client

    def send_email(self, source_address=str, destination_address=str, content=str):
        try:
            self.client.send_email(Destination={
                'ToAddresses': [destination_address]
            },
                Message={

                    'Body': {
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': content,
                        }
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': 'Test email',
                    },
                },
                Source=source_address
            )
        except Exception as e:
            raise MailServiceError(message="An error occurred when mail client was called.", cause=e)



