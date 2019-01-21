import unittest
from transaction import Transaction
from data_operation import DataOperation
import data_generator
import uuid

class TransactionTest(unittest.TestCase):
    def test_constructor_id(self):
        with self.assertRaises(ValueError) as context:
            Transaction('1234')

        self.assertEqual('id must be of type int', str(context.exception))

    def test_transaction_id_counter(self): 
        txs = []

        for i in range(5):
            txs.append(Transaction())

        for idx, tx in enumerate(txs):
            self.assertEqual(tx.id, idx + 1)
        
        self.assertEqual(Transaction.id_counter, 5)

    def test_add_invalid_data_operation(self):
        tx = Transaction(1)

        #with self.assertRaises(Exception) as context:
          #  tx.add_data_operation("test")

    def test_validate_no_ops(self):
        tx = Transaction(1)

        with self.assertRaises(Exception) as context:
            tx.validate()

        self.assertEqual('transaction must have at least one read/write data operation and one abort/commit operation', str(context.exception))

    def test_validate_no_commit_abort(self):
        tx = Transaction(1)
        tx.add_data_operation(data_generator.make_data_read_operation())
        
        with self.assertRaises(Exception) as context:
            tx.validate()
       
        self.assertEqual('transaction must have at least one read/write data operation and one abort/commit operation', str(context.exception))                                                                                                                                                                             

if __name__ == '__main__':
    unittest.main()