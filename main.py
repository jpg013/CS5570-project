from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import DataGeneration
from recovery_engine import RecoveryEngine
from serializable_or_not import serializable_or_not
from serialization_graphics import drawSerializationGraph
from app_config import AppConfig

def checks(hist):
    recovery_engine = RecoveryEngine(hist)
    report = recovery_engine.get_report()
    report.display_pretty()

    temp = serializable_or_not(hist)
    
    if(temp[0]):
        print("The history is serializable", end = "\n")
    else:
        print("The history is not serializable", end = "\n")
    return (report, temp)

def main():
    input_str = "w1[x] r2[x] w2[x] w1[x] c1 c2"
    history = HistoryQueryBuilder(input_str).process()
    recovery_engine = RecoveryEngine(history)
    report = recovery_engine.get_report()
    report.display_pretty()
    #data_generation = DataGeneration()
    #history = History(data_generation.generate_transactions())
    #history.interleave_transaction_schedule()
    #recovery_engine = RecoveryEngine(history)
    #report = recovery_engine.get_report()
    #report.display_pretty()
    
if __name__== "__main__":
    main()