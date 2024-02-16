from decode_function import BucketReader
from mail_client import MailService
from dynamo_client import DynamoClient
from datetime import datetime
from flask import Flask, jsonify, request
import awsgi
import json

app = Flask("DailymailStack")


@app.route('/', methods=['POST'])
def send_email():
    data = json.loads(request.get_data().decode('utf-8'))
    bucket = data["bucket"]
    address = data["address"]
    content = data["content"]
    current_date = datetime.today().strftime('%Y.%m.%d.%H.%M.%S')
    content_str = BucketReader().read_object_content(bucket=bucket, object_key=content)
    DynamoClient(table="DailyTable").dynamo_put_item(item={"email": address, "date": current_date, "content": content})
    MailService().send_email(source_address=address, destination_address=address, content=content_str)
    return jsonify(status=200, message="Email sent")


def lambda_handler(event, context):
    return awsgi.response(app, event, context)
