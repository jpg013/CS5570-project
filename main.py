from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import generate_transactions
from recovery_engine import RecoveryEngine
from serializable_or_not import serializable_or_not
from serialization_graphics import drawSerializationGraph

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
    not_recoverable_hist_input = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] c2 w1[z] c1'
    not_recoverable_hist = HistoryQueryBuilder(not_recoverable_hist_input).process()
    
    checks(not_recoverable_hist)
    
    recoverable_not_aca_input = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] w1[z] c1 c2'
    recoverable_not_aca_hist = HistoryQueryBuilder(recoverable_not_aca_input).process()

    checks(recoverable_not_aca_hist)
 
    aca_not_strict_input = 'w1[x] w1[y] r2[u] w2[x] w1[z] c1 r2[y] w2[y] c2'
    aca_not_strict_hist = HistoryQueryBuilder(aca_not_strict_input).process()

    checks(aca_not_strict_hist)

    strict_input = 'r1[x] w1[x] c1 r2[x] w2[x] c2'
    strict_hist = HistoryQueryBuilder(strict_input).process()

    checks(strict_hist)

    not_serializable_input = "w1[x] w2[x] w2[y] c2 w1[y] w3[x] w3[y] c3 c1"
    not_serializable_hist = HistoryQueryBuilder(not_serializable_input).process()
    not_serializable_hist.print_pretty()

    checks(not_serializable_hist)
    
if __name__== "__main__":
    main()

    hist = HistoryQueryBuilder('w1231[q] r11[r] a231 c11').process()
    checks(hist)

    """
    total_num = 1000
    num_recoverable = 0
    num_aca = 0
    num_strict = 0

    for i in range(total_num):
        history_transactions = generate_transactions()
        hist = History(history_transactions)
        hist.interleave_transaction_schedule()   
        recovery_engine = RecoveryEngine(hist)
        report = recovery_engine.get_report()
        
        if report.is_recoverable():
            num_recoverable += 1

        if report.is_aca():
            num_aca += 1

        if report.is_strict():
            num_strict += 1

    print(num_recoverable)
    print(num_aca)
    print(num_strict)
    """
