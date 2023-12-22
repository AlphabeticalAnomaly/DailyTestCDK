import boto3
from abc import ABC, abstractmethod


class IBucketReader(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read_object_content(self, params=dict):
        pass


class BucketReader(IBucketReader):
    def __init__(self):
        self.s3 = boto3.client("s3")

    def read_object_content(self, params=dict):
        bucket_object = self.s3.get_object(Bucket=params[0], Key=params[1])
        object_data = bucket_object['Body'].read()
        object_str = object_data.decode('utf-8')
        return object_str
