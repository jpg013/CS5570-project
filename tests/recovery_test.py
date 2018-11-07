import unittest
from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import DataGeneration
from recovery_engine import RecoveryEngine
from app_config import AppConfig

class RecoveryTest (unittest.TestCase):
  def test_not_recoverable(self):
    input_str = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] c2 w1[z] c1'
    history = HistoryQueryBuilder(input_str).process()
    recovery_engine = RecoveryEngine(history)
    report = recovery_engine.get_report()

    self.assertFalse(report.is_recoverable())
    self.assertFalse(report.is_aca())
    self.assertFalse(report.is_strict())

  def test_recoverable_not_aca(self):
    input_str = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] w1[z] c1 c2'
    history = HistoryQueryBuilder(input_str).process()
    recovery_engine = RecoveryEngine(history)
    report = recovery_engine.get_report()

    self.assertTrue(report.is_recoverable())
    self.assertFalse(report.is_aca())
    self.assertFalse(report.is_strict())
  
  def test_aca_not_strict(self):
    input_str = 'w1[x] w1[y] r2[u] w2[x] w1[z] c1 r2[y] w2[y] c2'
    history = HistoryQueryBuilder(input_str).process()
    recovery_engine = RecoveryEngine(history)
    report = recovery_engine.get_report()

    self.assertTrue(report.is_recoverable())
    self.assertTrue(report.is_aca())
    self.assertFalse(report.is_strict())
  
  def test_strict(self):
    input_str = 'r1[x] w1[x] c1 r2[x] w2[x] c2'
    history = HistoryQueryBuilder(input_str).process()
    recovery_engine = RecoveryEngine(history)
    report = recovery_engine.get_report()

    self.assertTrue(report.is_recoverable())
    self.assertTrue(report.is_aca())
    self.assertTrue(report.is_strict())
  
if __name__ == '__main__':
  unittest.main()

  