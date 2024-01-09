from abc import ABC, abstractmethod
import boto3


def send_default_mail(address):
    boto3.client('ses').send_email(Destination={
            'ToAddresses': address
        },
            Message={

                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': "An error occurred when trying to call the mail client.",
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Test email',
                },
            },
            Source=address
        )


class MailServiceError(Exception):
    def __init__(self, error, exp):
        self.error = error
        self.exception = exp


class IMailService(ABC):

    @abstractmethod
    def send_email(self, source_address=str, destination_address=str, content=str):
        pass


class MailService(IMailService):

    def __init__(self):
        self.client = boto3.client('ses')

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
            send_default_mail(address="defaultaddress@email.com")
            raise MailServiceError(error="An error occurred when mail client was called.", exp=e)

