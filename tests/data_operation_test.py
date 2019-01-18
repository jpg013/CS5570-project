import unittest
from data_operation import DataOperation
from data_operation import OperationType
import uuid

class DataOperationTest(unittest.TestCase):
    def test_operation_type_arg(self):
        with self.assertRaises(ValueError) as context:
            DataOperation('data_operation', 'data_item')

        self.assertEqual('operation_type must be of type OperationType.', str(context.exception))

    def test_data_item_set(self):
        data_op = DataOperation(OperationType.READ, 'x')
        self.assertEqual('x', data_op.data_item)        

    def test_unique_uuid(self):
        data_op = DataOperation(OperationType.READ, 'x')
        self.assertTrue(isinstance(data_op.id, uuid.UUID))

    def test_write_op(self):
        data_op = DataOperation(OperationType.WRITE, 'x')
        
        self.assertTrue(data_op.is_write())
        self.assertFalse(data_op.is_commit())
        self.assertFalse(data_op.is_abort())
        self.assertFalse(data_op.is_read())
        self.assertEqual(data_op.to_string(), 'write[x]')
        self.assertEqual(data_op.to_json(), '{"operation_type": "WRITE", "data_item": "x"}')

    def test_read_op(self):
        data_op = DataOperation(OperationType.READ, 'y')
        
        self.assertTrue(data_op.is_read())
        self.assertFalse(data_op.is_commit())
        self.assertFalse(data_op.is_abort())
        self.assertFalse(data_op.is_write())
        self.assertEqual(data_op.to_string(), 'read[y]')
        self.assertEqual(data_op.to_json(), '{"operation_type": "READ", "data_item": "y"}')

    def test_commit_op(self):
        data_op = DataOperation(OperationType.COMMIT)
        
        self.assertTrue(data_op.is_commit())
        self.assertFalse(data_op.is_read())
        self.assertFalse(data_op.is_abort())
        self.assertFalse(data_op.is_write())
        self.assertEqual(data_op.to_string(), 'commit')
        self.assertEqual(data_op.to_json(), '{"operation_type": "COMMIT"}')
    
    def test_abort_op(self):
        data_op = DataOperation(OperationType.ABORT)
        
        self.assertTrue(data_op.is_abort())
        self.assertFalse(data_op.is_read())
        self.assertFalse(data_op.is_commit())
        self.assertFalse(data_op.is_write())
        self.assertEqual(data_op.to_string(), 'abort')
        self.assertEqual(data_op.to_json(), '{"operation_type": "ABORT"}')

if __name__ == '__main__':
    unittest.main()

  