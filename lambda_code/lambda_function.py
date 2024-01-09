from decode_function import BucketReader
from mail_client import MailService


def lambda_handler(event, context):
    bucket_reader = BucketReader()
    mail_sender = MailService()
    address_str = event["address"]
    content_str = bucket_reader.read_object_content(bucket=event["bucket"], object_key=event["content"])
    mail_sender.send_email(source_address=address_str, destination_address=address_str, content=content_str)
