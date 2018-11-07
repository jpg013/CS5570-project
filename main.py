from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import DataGeneration
from recovery_engine import RecoveryEngine
from serializable_or_not import serializable_or_not
from app_config import AppConfig
import matplotlib.pyplot as plt

def checks(hist):
    recovery_engine = RecoveryEngine(hist)
    report = recovery_engine.get_report()
    report.display_pretty()

    if(serializable_or_not(hist)):
        print("The history is serializable", end = "\n")
    else:
        print("The history is not serializable", end = "\n")

def main():
    input_str = "w1[x] c1 r2[x] w2[x] a2"
    history = HistoryQueryBuilder(input_str).process()
    recovery_engine = RecoveryEngine(history)
    report = recovery_engine.get_report()
    report.display_pretty()
    
if __name__== "__main__":
    main()