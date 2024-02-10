from decode_function import BucketReader
from mail_client import MailService
from dynamo_client import DynamoClient
from datetime import datetime


def lambda_handler(event, context, reader=BucketReader(), mailer=MailService(), dynamo=DynamoClient(table="DailyTable")):
    if 'queryStringParameters' in event:
        event = event['queryStringParameters']
    else:
        event = event
    current_date = datetime.today().strftime('%Y.%m.%d.%H.%M.%S')
    content_str = reader.read_object_content(bucket=event["bucket"], object_key=event["content"])
    mailer.send_email(source_address=event["address"], destination_address=event["address"], content=content_str)
    dynamo.dynamo_put_item(item={"email": event["address"], "date": current_date, "content": event["content"]})
    message = {
        'message': 'Email sent!'
    }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': message['message']
    }

