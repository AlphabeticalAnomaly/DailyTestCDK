from flask import Flask, request, jsonify
import awsgi
import json
from emailing_service import EmailingService


app = Flask("DailymailStack")


@app.route('/', methods=['POST'])
def send_email():
    data = json.loads(request.get_data().decode('utf-8'))
    EmailingService(data=data).send_email()
    return jsonify(status=200, message="Email sent")


def lambda_handler(event, context):
    return awsgi.response(app, event, context)
