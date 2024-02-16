from decode_function import BucketReader
from mail_client import MailService
from dynamo_client import DynamoClient
from datetime import datetime
from flask import Flask, jsonify
import awsgi

app = Flask("DailymailStack")
message = {
    'message': 'Email sent!'
}


@app.route('/', methods=['POST'])
def index():
    return jsonify(status=200, message='Email sent')


def lambda_handler(event, context, reader=BucketReader(), mailer=MailService(),
                   dynamo=DynamoClient(table="DailyTable")):
    if "headers" in event and bool(event["headers"]) != False:
        event_r = event["headers"]
        api_response = True
    elif "queryStringParameters" in event and bool(event["queryStringParameters"]) != False:
        event_r = event["queryStringParameters"]
        api_response = True
    else:
        event_r = event
        api_response = False
    current_date = datetime.today().strftime('%Y.%m.%d.%H.%M.%S')
    content_str = reader.read_object_content(bucket=event_r["bucket"], object_key=event_r["content"])
    mailer.send_email(source_address=event_r["address"], destination_address=event_r["address"], content=content_str)
    dynamo.dynamo_put_item(item={"email": event_r["address"], "date": current_date, "content": event_r["content"]})
    if api_response:
        return awsgi.response(app, event, context)
