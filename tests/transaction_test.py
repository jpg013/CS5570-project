import unittest
from data.data_operation import DataOperation
from data.data_operation import OperationType
import uuid

class DataOperationTest(unittest.TestCase):
    def test_operation_type_arg(self):
        with self.assertRaises(ValueError) as context:
            DataOperation('data_operation', 'data_item')

        self.assertEqual('operation_type must be of type OperationType.', str(context.exception))

    def test_transaction_id_arg(self):
        with self.assertRaises(ValueError) as context:
            DataOperation(OperationType.READ, 'data_item')

        self.assertEqual('transaction_id must be of type int', str(context.exception))

    def test_data_item_set(self):
        data_op = DataOperation(OperationType.READ, 1, 'x')
        self.assertEqual('x', data_op.data_item)        

    def test_unique_uuid(self):
        data_op = DataOperation(OperationType.READ, 1, 'x')
        self.assertTrue(isinstance(data_op.id, uuid.UUID))

if __name__ == '__main__':
    unittest.main()

  