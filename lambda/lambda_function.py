import boto3
from decode_function import object_body_to_str
ses = boto3.client('ses')


def lambda_handler(event, context):
    bucket = event["bucket"]
    address = event["address"]
    content = event["content"]
    address_str = object_body_to_str(bucket_name=bucket, object_key=address)
    content_str = object_body_to_str(bucket_name=bucket, object_key=content)
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

