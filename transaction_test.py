import unittest
from transaction import Transaction
from enum import Enum

class TransactionTest (unittest.TestCase):
  def test_fails_without_id(self):
    #tx = Transaction()
    #self.assertTrue(issubclass(transaction.operatoin, Enum))

  def test_enum_members(self):
    print('hello')
    #self.assertIsNotNone(transaction.OperationType.READ)
    #self.assertIsNotNone(transaction.OperationType.WRITE)
    #self.assertIsNotNone(transaction.OperationType.COMMIT)
    #self.assertIsNotNone(transaction.OperationType.ABORT)

  def test_has_value(self):
    print('world')
    #self.assertFalse(transaction.OperationType.has_value('bad_value'))
    #self.assertTrue(transaction.OperationType.has_value(transaction.OperationType.READ))
    #self.assertTrue(transaction.OperationType.has_value(transaction.OperationType.WRITE))
    #self.assertTrue(transaction.OperationType.has_value(transaction.OperationType.COMMIT))
    #self.assertTrue(transaction.OperationType.has_value(transaction.OperationType.ABORT))

if __name__ == '__main__':
  unittest.main()

  