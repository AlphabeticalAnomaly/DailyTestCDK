from abc import ABC, abstractmethod
import boto3


class BucketReaderError(Exception):
    def __init__(self, error, exp):
        self.error = error
        self.exception = exp


class IBucketReader(ABC):
    @abstractmethod
    def read_object_content(self, bucket=object, object_key=str):
        pass


class BucketReader(IBucketReader):

    def __init__(self):
        self.s3 = boto3.client('s3')
        self.object_str = str

    def read_object_content(self, bucket=object, object_key=str):
        try:
            bucket_object = self.s3.get_object(Bucket=bucket, Key=object_key)
        except Exception as e:
            self.object_str = "Bucket content could not be accessed properly."
            raise BucketReaderError(error="An error occurred when trying to access the content.", exp=e)

        try:
            object_data = bucket_object['Body'].read()
        except TypeError as e:
            raise BucketReaderError(error="An error occurred when trying to access the object's contents.", exp=e)

        try:
            self.object_str = object_data.decode('utf-8')
        except AttributeError as e:
            raise BucketReaderError(error='An error occurred when trying to decode the content.', exp=e)

        finally:
            return self.object_str
