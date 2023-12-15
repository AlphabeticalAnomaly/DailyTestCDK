import boto3


def object_body_to_str(bucket_name=str, object_key=str):
    s3 = boto3.client('s3')
    bucket_object = s3.get_object(Bucket=bucket_name, Key=object_key)
    object_data = bucket_object['Body'].read()
    object_str = object_data.decode('utf-8')
    return object_str
