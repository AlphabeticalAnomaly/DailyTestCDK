from abc import ABC, abstractmethod
import boto3.session


class BucketReaderError(Exception):
    def __init__(self, message, cause):
        self.error = message
        self.cause = cause


class IBucketReader(ABC):
    @abstractmethod
    def read_object_content(self, bucket=str, object_key=str):
        pass


class BucketReader(IBucketReader):
    def __init__(self, client=boto3.client('s3')):
        self.s3 = client

    def read_object_content(self, bucket=str, object_key=str):
        bucket_object = self.__read_bucket_object(bucket, object_key)
        object_data = self.__read_object_data(bucket_object)
        return self.__decode_object_data(object_data)

    def __read_bucket_object(self, bucket=str, object_key=str):
        try:
            return self.s3.get_object(Bucket=bucket, Key=object_key)
        except Exception as e:
            raise BucketReaderError(message="An error occurred when trying to access the content.", cause=e)

    def __read_object_data(self, bucket_object):
        try:
            return bucket_object['Body'].read()
        except Exception as e:
            raise BucketReaderError(message="An error occurred when trying to access the object's contents.", cause=e)

    def __decode_object_data(self, object_data):
        try:
            return object_data.decode('utf-8')
        except Exception as e:
            raise BucketReaderError(message='An error occurred when trying to decode the content.', cause=e)
