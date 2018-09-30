import unittest
import transaction
from enum import Enum

class OperationTypeTest (unittest.TestCase):
  def test_class(self):
    self.assertTrue(issubclass(transaction.OperationType, Enum))

  def test_enum_members(self):
    self.assertIsNotNone(transaction.OperationType.READ)
    self.assertIsNotNone(transaction.OperationType.WRITE)
    self.assertIsNotNone(transaction.OperationType.COMMIT)
    self.assertIsNotNone(transaction.OperationType.ABORT)

  def test_has_value(self):
    self.assertFalse(transaction.OperationType.has_value('bad_value'))
    self.assertTrue(transaction.OperationType.has_value(transaction.OperationType.READ))
    self.assertTrue(transaction.OperationType.has_value(transaction.OperationType.WRITE))
    self.assertTrue(transaction.OperationType.has_value(transaction.OperationType.COMMIT))
    self.assertTrue(transaction.OperationType.has_value(transaction.OperationType.ABORT))

if __name__ == '__main__':
  unittest.main()

  