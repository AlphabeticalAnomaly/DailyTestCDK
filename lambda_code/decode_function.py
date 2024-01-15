from abc import ABC, abstractmethod
import boto3.session


class BucketReaderError(Exception):
    def __init__(self, error, exp):
        self.error = error
        self.cause = exp


class IBucketReader(ABC):
    @abstractmethod
    def read_object_content(self, bucket=str, object_key=str):
        pass


class BucketReader(IBucketReader):
    def __init__(self, session=boto3.session.Session()):
        self.s3 = session.client(service_name='s3', region_name='eu-north-1')

    def read_object_content(self, bucket=str, object_key=str):
        bucket_object = self.__read_bucket_object(bucket, object_key)
        object_data = self.__read_object_data(bucket_object)
        return self.__decode_object_data(object_data)

    def __read_bucket_object(self, bucket=str, object_key=str):
        try:
            return self.s3.get_object(Bucket=bucket, Key=object_key)
        except Exception as e:
            raise BucketReaderError(error="An error occurred when trying to access the content.", exp=e)

    def __read_object_data(self, bucket_object):
        try:
            return bucket_object['Body'].read()
        except Exception as e:
            raise BucketReaderError(error="An error occurred when trying to access the object's contents.", exp=e)

    def __decode_object_data(self, object_data):
        try:
            return object_data.decode('utf-8')
        except Exception as e:
            raise BucketReaderError(error='An error occurred when trying to decode the content.', exp=e)





