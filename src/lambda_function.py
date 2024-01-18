from src.decode_function import BucketReader
from src.mail_client import MailService
import sys


def read(bucket, object_key):
    return BucketReader().read_object_content(bucket=bucket, object_key=object_key)


def mail(source_address, destination_address, content):
    return MailService().send_email(source_address=source_address, destination_address=destination_address, content=content)


def lambda_handler(event, context):
    address_str = event["address"]
    content_str = read(bucket=event["bucket"], object_key=event["content"])
    mail(source_address=address_str, destination_address=address_str, content=content_str)






