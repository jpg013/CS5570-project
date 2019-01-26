import unittest
from data_operation import DataOperation, OperationType
import data_generator
import uuid

class DataOperationTest(unittest.TestCase):
    def test_operation_type_constructor(self):
        op = DataOperation(
            data_generator.get_transaction_cardinality(), 
            OperationType.READ
        )
        
        self.assertTrue(isinstance(op, DataOperation))
    
    def test_data_item_set(self):
        data_op = DataOperation(
            data_generator.get_transaction_cardinality(),     
            OperationType.READ, 
            'x'
        )
        self.assertEqual('x', data_op.data_item)        

    def test_unique_uuid(self):
        data_op = data_generator.make_data_read_operation()
        self.assertTrue(isinstance(data_op.id, uuid.UUID))
    
    def test_write_op(self):
        tx_id = 1
        data_item = "x"

        data_op = DataOperation(
            tx_id,
            OperationType.WRITE, 
            data_item
        )
        
        self.assertTrue(data_op.is_write())
        self.assertFalse(data_op.is_commit())
        self.assertFalse(data_op.is_abort())
        self.assertFalse(data_op.is_read())
        self.assertEqual(data_op.to_string(), 'write_1[x]')
        self.assertEqual(data_op.to_json(), '{"operation_type": "WRITE", "transaction_id": 1, "data_item": "x"}')

    def test_read_op(self):
        tx_id = 2
        data_item = "y"

        data_op = DataOperation(
            tx_id,
            OperationType.READ, 
            data_item
        )
        
        self.assertTrue(data_op.is_read())
        self.assertFalse(data_op.is_commit())
        self.assertFalse(data_op.is_abort())
        self.assertFalse(data_op.is_write())
        self.assertEqual(data_op.to_string(), 'read_2[y]')
        self.assertEqual(data_op.to_json(), '{"operation_type": "READ", "transaction_id": 2, "data_item": "y"}')

    def test_commit_op(self):
        tx_id = 3

        data_op = DataOperation(
            tx_id,
            OperationType.COMMIT, 
        )
        
        self.assertTrue(data_op.is_commit())
        self.assertFalse(data_op.is_read())
        self.assertFalse(data_op.is_abort())
        self.assertFalse(data_op.is_write())
        self.assertEqual(data_op.to_string(), 'commit_3')
        self.assertEqual(data_op.to_json(), '{"operation_type": "COMMIT", "transaction_id": 3}')
    
    def test_abort_op(self):
        tx_id = 4

        data_op = DataOperation(
            tx_id,
            OperationType.ABORT, 
        )
        
        self.assertTrue(data_op.is_abort())
        self.assertFalse(data_op.is_read())
        self.assertFalse(data_op.is_commit())
        self.assertFalse(data_op.is_write())
        self.assertEqual(data_op.to_string(), 'abort_4')
        self.assertEqual(data_op.to_json(), '{"operation_type": "ABORT", "transaction_id": 4}')

if __name__ == '__main__':
    unittest.main()

  