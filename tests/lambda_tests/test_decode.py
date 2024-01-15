import unittest
from lambda_code.decode_function import BucketReader, BucketReaderError
from unittest.mock import Mock


class TestSomething(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()
        self.bucket_reader = BucketReader(self.mock_session)
        self.bucket_reader.s3 = Mock()
        self.object_content = Mock()
        self.object_data = Mock()
        self.object_content.read.return_value = bytes('content', 'utf-8')
        self.dictionary = {'Body': self.object_content}

    def test_reader(self):
        self.bucket_reader.s3.get_object.return_value = self.dictionary
        self.bucket_reader.read_object_content(bucket="bucket", object_key="key")
        self.bucket_reader.s3.get_object.assert_called_once_with(Bucket="bucket", Key="key")

    def test_get_object_side_effect(self):
        expected_exception = Exception('exception')
        self.bucket_reader.s3.get_object.side_effect = expected_exception
        with self.assertRaises(BucketReaderError) as context:
            self.bucket_reader.read_object_content(bucket="bucket", object_key="key")
        self.assertEqual('An error occurred when trying to access the content.', context.exception.error)
        self.assertEqual(expected_exception, context.exception.cause)

    def test_read_side_effect(self):
        expected_exception = Exception('exception')
        self.object_content.read.side_effect = expected_exception
        self.bucket_reader.s3.get_object.return_value = self.dictionary
        with self.assertRaises(BucketReaderError) as context:
            self.bucket_reader.read_object_content(bucket="bucket", object_key="key")
        self.assertEqual("An error occurred when trying to access the object's contents.", context.exception.error)
        self.assertEqual(expected_exception, context.exception.cause)

    def test_decode_side_effect(self):
        expected_exception = Exception('exception')
        self.object_content.read.return_value = self.object_data
        self.object_data.decode.side_effect = expected_exception
        self.bucket_reader.s3.get_object.return_value = self.dictionary
        with self.assertRaises(BucketReaderError) as context:
            self.bucket_reader.read_object_content(bucket="bucket", object_key="key")
        self.assertEqual('An error occurred when trying to decode the content.', context.exception.error)
        self.assertEqual(expected_exception, context.exception.cause)
