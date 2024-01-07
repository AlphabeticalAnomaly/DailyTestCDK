from abc import ABC, abstractmethod
import boto3


class MailServiceError(Exception):
    def __init__(self, error, exp):
        self.error = error
        self.exception = exp


class IMailService(ABC):

    @abstractmethod
    def send_mail(self, source_address=str, destination_address=str, content=str):
        pass


class MailService(IMailService):

    def __init__(self):
        self.client = boto3.client('ses')
        self.default_email = "defaultaddress@email.com"

    def send_mail(self, source_address=str, destination_address=str, content=str):
        try:
            self.client.send_mail(Destination={
                'ToAddresses': destination_address
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
            self.client.send_mail(Destination={
                'ToAddresses': self.default_email
            },
                Message={

                    'Body': {
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': "An error occurred when mail client was called.",
                        }
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': 'Test email',
                    },
                },
                Source=self.default_email
            )
            raise MailServiceError(error="An error occurred when mail client was called.", exp=e)

