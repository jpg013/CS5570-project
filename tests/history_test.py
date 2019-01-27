import unittest
from data_operation import DataOperation, OperationType
import data_generator
import uuid

class HistoryTest(unittest.TestCase):
    def test_operation_type_constructor(self):
        op = DataOperation(
            data_generator.get_transaction_cardinality(), 
            OperationType.READ
        )
        
        self.assertTrue(isinstance(op, DataOperation))

if __name__ == '__main__':
    unittest.main()

  