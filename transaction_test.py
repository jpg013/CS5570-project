import unittest
from transaction import Transaction

class TransactionTest(unittest.TestCase):
  def setUp(self):
    self.tx = Transaction()

  def test_transaction_defaults(self):
    # verify defaults 
    self.assertEqual(self.tx.commit_on_complete, True)
    self.assertGreaterEqual(self.tx.data_item_count, 1)
    self.assertLessEqual(self.tx.data_item_count, 4)

if __name__ == '__main__':
  unittest.main()

  