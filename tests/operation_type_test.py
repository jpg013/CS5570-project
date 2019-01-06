import unittest
from data.operation_type import OperationType, type_switcher

class OperationTypeTest(unittest.TestCase):
    def test_attributes(self):
        self.assertIsNotNone(OperationType.READ)
        self.assertIsNotNone(OperationType.WRITE)
        self.assertIsNotNone(OperationType.COMMIT)
        self.assertIsNotNone(OperationType.ABORT)

    def test_has_value_read(self):
        self.assertTrue(OperationType.has_value(OperationType.READ))
    
    def test_has_value_write(self):
        self.assertTrue(OperationType.has_value(OperationType.WRITE))

    def test_has_value_commit(self):
        self.assertTrue(OperationType.has_value(OperationType.COMMIT))

    def test_has_value_abort(self):
        self.assertTrue(OperationType.has_value(OperationType.ABORT))

    def test_invalid_value(self):
        self.assertFalse(OperationType.has_value('invalid'))

    def test_type_switcher(self):
        self.assertEqual(type_switcher[0], OperationType.READ)
        self.assertEqual(type_switcher[1], OperationType.WRITE)
        self.assertEqual(type_switcher[2], OperationType.COMMIT)
        self.assertEqual(type_switcher[3], OperationType.ABORT)

if __name__ == '__main__':
    unittest.main()

  