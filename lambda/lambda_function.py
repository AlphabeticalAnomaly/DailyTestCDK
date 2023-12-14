import boto3
ses = boto3.client('ses')
s3 = boto3.client('s3')


def lambda_handler(event, context):
    bucket = event["bucket"]
    address = event["address"]
    content = event["content"]
    response_address = s3.get_object(Bucket=bucket, Key=address)
    address_data = response_address['Body'].read()
    address_str = address_data.decode('utf-8')
    response_content = s3.get_object(Bucket=bucket, Key=content)
    content_data = response_content['Body'].read()
    content_str = content_data.decode('utf-8')

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

