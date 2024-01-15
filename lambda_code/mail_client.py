from abc import ABC, abstractmethod
import boto3.session


class MailServiceError(Exception):
    def __init__(self, error, exp):
        self.error = error
        self.cause = exp


class IMailService(ABC):

    @abstractmethod
    def send_email(self, source_address=str, destination_address=str, content=str):
        pass


class MailService(IMailService):

    def __init__(self, session=boto3.session.Session()):
        self.client = session.client(service_name='ses', region_name='eu-north-1')

    def send_email(self, source_address=str, destination_address=str, content=str):
        self.__send_email(source_address=source_address, destination_address=destination_address, content=content)

    def __send_email(self, source_address, destination_address, content):
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
            raise MailServiceError(error="An error occurred when mail client was called.", exp=e)


