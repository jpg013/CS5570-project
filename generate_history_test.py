import unittest
import generate_history

class MyTest(unittest.TestCase):
  def test(self):
    self.assertEqual(generate_history.fun(3), 4)

if __name__ == '__main__':
  unittest.main()