from decode_function import BucketReader
from mail_client import MailService
from dynamo_client import DynamoClient
from datetime import datetime
from abc import ABC, abstractmethod


class ISendEmail(ABC):
    @abstractmethod
    def send_email(self, bucket, content, address):
        pass


class EmailingService(ISendEmail):
    def __init__(self, reader=BucketReader(), mailer=MailService(), dynamo=DynamoClient(table="DailyTable")):
        self.reader = reader
        self.mailer = mailer
        self.dynamo = dynamo
        self.current_date = datetime.today().strftime('%Y.%m.%d.%H.%M.%S')
        self.content_str = str

    def send_email(self, bucket, content, address):
        self.content_str = self.reader.read_object_content(bucket=bucket, object_key=content)
        self.dynamo.dynamo_put_item(item={"email": address, "date": self.current_date, "content": content})
        self.mailer.send_email(source_address=address, destination_address=address, content=self.content_str)
