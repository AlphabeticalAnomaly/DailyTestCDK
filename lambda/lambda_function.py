import boto3
from decode_function import BucketReader
ses = boto3.client('ses')


def lambda_handler(event, context):
    bucket = event["bucket"]
    address = event["address"]
    content = event["content"]
    reader = BucketReader()
    address_str = reader.read_object_content(bucket_name=bucket, object_key=address)
    content_str = reader.read_object_content(bucket_name=bucket, object_key=content)
    mail = ses.send_email(Destination={
        'ToAddresses': [address_str]
    },
        Message={

            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': content_str,
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Test email',
            },
        },
        Source=address_str
    )

