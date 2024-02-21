from flask import Flask, request, jsonify
import awsgi
import json
from emailing_service import EmailingService

BUCKET_KEY = "bucket"
ADDRESS_KEY = "address"
CONTENT_KEY = "content"
KEY_LIST = [BUCKET_KEY, ADDRESS_KEY, CONTENT_KEY]

app = Flask("DailymailStack")
email_service = EmailingService()


@app.route('/', methods=['POST'])
def send_email():
    data = json.loads(request.get_data().decode('utf-8'))
    keysNotFound = [key for key in KEY_LIST if key not in data]
    if keysNotFound != 0:
        return jsonify(status=400, message=f"The following keys: {keysNotFound}, were not found in the request")
    else:
        email_service.send_email(bucket=data[BUCKET_KEY], content=data[CONTENT_KEY], address=data[ADDRESS_KEY])
        return jsonify(status=200, message="Email sent!y")


def lambda_handler(event, context):
    try:
        return awsgi.response(app, event, context)
    except Exception as e:
        return jsonify(status=500, message="The server encountered an error.")
