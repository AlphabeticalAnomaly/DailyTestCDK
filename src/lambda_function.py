from decode_function import BucketReader
from mail_client import MailService


def lambda_handler(event, context, reader=BucketReader(), mailer=MailService()):
    content_str = reader.read_object_content(bucket=event["bucket"], object_key=event["content"])
    mailer.send_email(source_address=event["address"], destination_address=event["address"], content=content_str)
