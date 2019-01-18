import unittest
from transaction import Transaction
from data_operation import DataOperation
import uuid

class TransactionTest(unittest.TestCase):
    def test_constructor_id(self):
        with self.assertRaises(ValueError) as context:
            Transaction('1234')

        self.assertEqual('id must be of type int', str(context.exception))

    def test_validate_no_ops(self):
        tx = Transaction(1)

        with self.assertRaises(Exception) as context:
            tx.validate()

        self.assertEqual('transaction must have at least one read/write data operation and one abort/commit operation', str(context.exception))

    # def test_validate_no_commit_abort(self):
        # tx 
    
if __name__ == '__main__':
    unittest.main()