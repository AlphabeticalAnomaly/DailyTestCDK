import unittest
from src.dynamo_client import DynamoClient, DynamoClientError
from unittest.mock import Mock


class TestDynamoClient(unittest.TestCase):
    def setUp(self):
        self.resource = Mock()
        self.dynamo = DynamoClient(resource=self.resource)
        self.dynamo.table = Mock()
        self.item = {"Object": "test_object", "Key": "test_key"}

    def test_put_item(self):
        self.dynamo.dynamo_put_item(item=self.item)
        self.dynamo.table.put_item.assert_called_with(Item={"Object": "test_object", "Key": "test_key"})

    def test_put_item_exception_handling(self):
        expected_exception = Exception
        self.dynamo.table.put_item.side_effect = expected_exception
        with self.assertRaises(DynamoClientError) as context:
            self.dynamo.dynamo_put_item(self.item)
        self.assertEqual("An error has occurred when trying to access the database.", context.exception.message)