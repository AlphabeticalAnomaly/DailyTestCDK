import boto3
from abc import ABC, abstractmethod
import os


class DynamoClientError(Exception):
    def __init__(self, message, cause):
        self.message = message
        self.cause = cause


class IDynamoClient(ABC):
    @abstractmethod
    def dynamo_put_item(self, item=dict):
        pass


class DynamoClient(IDynamoClient):
    def __init__(self, resource=boto3.resource('dynamodb', str(os.environ.get('AWS_REGION'))), table=str):
        self.dynamodb = resource
        self.table = self.dynamodb.Table(table)

    def dynamo_put_item(self, item=dict):
        try:
            self.table.put_item(Item=item)
        except Exception as e:
            raise DynamoClientError(message="An error has occurred when trying to access the database.", cause=e)


