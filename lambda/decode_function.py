from abc import ABC, abstractmethod
from containers import Container
from dependency_injector.wiring import inject, Provide


class IBucketReader(ABC):
    @abstractmethod
    def read_object_content(self, bucket=object, object_key=str):
        pass


class BucketReader(IBucketReader):
    @inject
    def __init__(self, boto3_client=Provide[Container.s3_client]):
        self.s3 = boto3_client

    def read_object_content(self, bucket=object, object_key=str):
        bucket_object = self.s3.get_object(Bucket=bucket, Key=object_key)
        object_data = bucket_object['Body'].read()
        object_str = object_data.decode('utf-8')
        return object_str
