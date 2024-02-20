from decode_function import BucketReader
from mail_client import MailService
from dynamo_client import DynamoClient
import json
from datetime import datetime


def send_email(data=dict, reader=BucketReader(), mailer=MailService(), dynamo=DynamoClient(table="DailyTable")):
    bucket = data["bucket"]
    address = data["address"]
    content = data["content"]
    current_date = datetime.today().strftime('%Y.%m.%d.%H.%M.%S')
    content_str = reader.read_object_content(bucket=bucket, object_key=content)
    dynamo.dynamo_put_item(item={"email": address, "date": current_date, "content": content})
    mailer.send_email(source_address=address, destination_address=address, content=content_str)
