from decode_function import BucketReader
from mail_client import MailService
from dynamo_client import DynamoClient
from datetime import datetime
from abc import ABC, abstractmethod


class ISendEmail(ABC):
    @abstractmethod
    def send_email(self):
        pass


class EmailingService(ISendEmail):
    def __init__(self, data=dict, reader=BucketReader(), mailer=MailService(), dynamo=DynamoClient(table="DailyTable")):
        self.reader = reader
        self.mailer = mailer
        self.dynamo = dynamo
        self.bucket = data["bucket"]
        self.address = data["address"]
        self.content = data["content"]
        self.current_date = datetime.today().strftime('%Y.%m.%d.%H.%M.%S')
        self.content_str = str

    def send_email(self):
        self.content_str = self.reader.read_object_content(bucket=self.bucket, object_key=self.content)
        self.dynamo.dynamo_put_item(item={"email": self.address, "date": self.current_date, "content": self.content})
        self.mailer.send_email(source_address=self.address, destination_address=self.address, content=self.content_str)
