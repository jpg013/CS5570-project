from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import generate_transactions
from transaction_recovery_engine import TransactionRecoveryEngine

def main():
    input_str = "w1(x) r2(x) c2 c1"

    hist = HistoryQueryBuilder(input_str).process()
    hist.pretty_print()
    
    #hist = History()
    #hist.add_transactions(generate_transactions()).randomize_schedule()

    #hist.pretty_print()
    
    recovery_engine = TransactionRecoveryEngine(hist)
    recovery_engine.analyze()
    #recoverable_result = r_engine.is_recoverable()
    
    #print(recoverable_result.message)

    #aca_result = r_engine.is_aca()
    #print(aca_result.message)
    
if __name__== "__main__":
    main()