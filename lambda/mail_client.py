from abc import ABC, abstractmethod
from containers import Container
from dependency_injector.wiring import inject, Provide


class IMailService(ABC):

    @abstractmethod
    def send_mail(self, source_address=str, destination_address=str, content=str):
        pass


class MailService(IMailService):
    @inject
    def __init__(self, boto3_client=Provide[Container.ses_client]):
        self.client = boto3_client

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
