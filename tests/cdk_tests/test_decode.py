import unittest
from lambda_code.decode_function import BucketReader
from unittest.mock import patch, Mock, MagicMock
import boto3


class BucketReaderTest(unittest.TestCase):
    @patch('BucketReader.read_object_content')
    def test_read_object_content(self, mock_get):
        mock_get(bucket="bucket", object_key="key")
        mock_get.assert_called_once()







