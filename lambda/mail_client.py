import boto3
from abc import ABC, abstractmethod


class IMailService(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def send_mail(self, source_address=str, destination_address=str, content=str):
        pass


class MailService(IMailService):
    def __init__(self):
        self.client = boto3.client('ses')

    def send_mail(self, source_address=str, destination_address=str, content=str):
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
