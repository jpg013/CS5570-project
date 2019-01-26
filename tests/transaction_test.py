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
    

    def test_validate_no_ops(self):
        tx = Transaction(1)

        with self.assertRaises(Exception) as context:
            tx.validate()

        self.assertEqual('transaction must have at least one read/write data operation and one abort/commit operation', str(context.exception))

    def test_validate_no_commit_abort(self):
        tx_id=1
        tx = Transaction(tx_id)
        tx.add_data_operation(data_generator.make_data_read_operation(tx_id))
        
        with self.assertRaises(Exception) as context:
            tx.validate()
       
        self.assertEqual('transaction must have at least one read/write data operation and one abort/commit operation', str(context.exception))                                                                                                                                                                             

    def test_validate_correct(self):
        tx_id=1
        tx = Transaction(tx_id)
        tx.add_data_operation(data_generator.make_data_read_operation(tx_id))
        tx.add_data_operation(data_generator.make_data_commit_operation(tx_id))
        tx.validate()

    def test_add_multiple_commits(self):
        tx_id = 1
        tx = Transaction(tx_id)
        tx.add_data_operation(data_generator.make_data_read_operation(tx_id))
        tx.add_data_operation(data_generator.make_data_commit_operation(tx_id))
        
        with self.assertRaises(Exception) as context:
            tx.add_data_operation(data_generator.make_data_commit_operation(tx_id))
        
        self.assertEqual('cannot add data_operation commit_1', str(context.exception))
    
    def test_add_data_operation_invalidate_tx(self):
        tx_id = 1
        tx_id_2 = 2
        tx = Transaction(tx_id)
        
        with self.assertRaises(Exception) as context:
            tx.add_data_operation(data_generator.make_data_read_operation(tx_id_2, 'y'))
        
        self.assertEqual('cannot add data_operation read_2[y]', str(context.exception))

if __name__ == '__main__':
    unittest.main()