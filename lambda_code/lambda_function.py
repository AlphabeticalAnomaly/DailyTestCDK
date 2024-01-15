from lambda_code.decode_function import BucketReader
from lambda_code.mail_client import MailService
import boto3


def read(bucket, object_key):
    reader = BucketReader(session=boto3.session.Session())
    try:
        return reader.read_object_content(bucket=bucket, object_key=object_key)
    except Exception as e:
        return "An error occurred when trying to access the bucket's contents."


def mail(source_address, destination_address, content):
    client = MailService(session=boto3.session.Session())
    try:
        client.send_email(source_address=source_address, destination_address=destination_address, content=content)
    except Exception as e:
        client.send_email(source_address="default@email.doimain", destination_address="default@email.doimain", content="An error occurred within the mail client.")


def lambda_handler(event, context):
    address_str = event["address"]
    content_str = read(bucket=event["bucket"], object_key=event["content"])
    mail(source_address=address_str, destination_address=address_str, content=content_str)





