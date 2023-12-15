import boto3


class BucketReader(boto3):
    def __init__(self):
        super().__init__()
        self.s3 = boto3.client("s3")

    def read_object_content(self, bucket_name=str, object_key=str):
        bucket_object = self.s3.get_object(Bucket=bucket_name, Key=object_key)
        object_data = bucket_object['Body'].read()
        object_str = object_data.decode('utf-8')
        return object_str
