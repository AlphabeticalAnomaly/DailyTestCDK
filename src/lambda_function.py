from flask import Flask, request, jsonify
import awsgi
import json
from app_task import send_email


app = Flask("DailymailStack")


@app.route('/', methods=['POST'])
def task():
    data = json.loads(request.get_data().decode('utf-8'))
    send_email(data=data)
    return jsonify(status=200, message="Email sent")


def lambda_handler(event, context):
    return awsgi.response(app, event, context)
