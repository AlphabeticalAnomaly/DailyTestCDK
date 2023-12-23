import boto3
from abc import ABC, abstractmethod


class IBucketReader(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read_object_content(self, bucket=object, object_key=str):
        pass


class BucketReader(IBucketReader):
    def __init__(self):
        self.s3 = boto3.client("s3")

    def read_object_content(self, bucket=object, object_key=str):
        bucket_object = self.s3.get_object(Bucket=bucket, Key=object_key)
        object_data = bucket_object['Body'].read()
        object_str = object_data.decode('utf-8')
        return object_str
