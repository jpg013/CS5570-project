import unittest
from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import DataGeneration
from recovery_engine import RecoveryEngine
from app_config import AppConfig


class RecoverTest (unittest.TestCase):
  def not_recoverable_history(self):
    input_str = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] c2 w1[z] c1'
    history = HistoryQueryBuilder(not_recoverable_hist_input).process()
    recovery_engine = RecoveryEngine(history)
    report = recovery_engine.get_report()

    self.assertFalse(report.is_recoverable())
    self.assertFalse(report.is_aca())
    self.assertFalse(report.is_strict())

if __name__ == '__main__':
  unittest.main()

  