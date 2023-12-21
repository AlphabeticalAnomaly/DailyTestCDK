from decode_function import BucketReader
from event_reader import EventReader
from mail_client import MailService


def lambda_handler(event, context):
    event_reader = EventReader(event)
    bucket_reader = BucketReader()
    mail_sender = MailService()
    address_str = bucket_reader.read_object_content(event_reader.get_object(key="address"))
    content_str = bucket_reader.read_object_content(event_reader.get_object(key="content"))
    mail_sender.send_mail(source_address=address_str, destination_address=address_str, content=content_str)
