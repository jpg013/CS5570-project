from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import generate_transactions
from recovery_engine import RecoveryEngine
from serializable_or_not import serializable_or_not

def checks(hist):
    recovery_engine = RecoveryEngine(hist)
    results = recovery_engine.analyze()
    print(results)

    # print("\n")

    # if(serializable_or_not(hist)):
        # print("The history is serializable", end = "\n")
    # else:
        # print("The history is not serializable", end = "\n")

def main():

    not_recoverable_hist_input = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] c2 w1[z] c1'
    not_recoverable_hist = HistoryQueryBuilder(not_recoverable_hist_input).process()
    
    checks(not_recoverable_hist)

    recoverable_not_aca_input = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] w1[z] c1 c2'
    recoverable_not_aca_hist = HistoryQueryBuilder(recoverable_not_aca_input).process()
    #recoverable_not_aca_hist.pretty_print()

    checks(recoverable_not_aca_hist)
 
    #aca_not_strict_input = 'w1[x] w1[y] r2[u] w2[x] w1[z] c1 r2[y] w2[y] c2'
    #aca_not_strict_hist = HistoryQueryBuilder(aca_not_strict_input).process()
    #aca_not_strict_hist.pretty_print()

    #checks(aca_not_strict_hist)

    #strict_input = 'r1[x] w1[x] c1 r2[x] w2[x] c2'
    #strict_hist = HistoryQueryBuilder(strict_input).process()
    #strict_hist.pretty_print()

    #checks(strict_hist)
    
    #not_serializable_input = "w1[x] w2[x] w2[y] c2 w1[y] w3[x] w3[y] c3 c1"
    #not_serializable_hist = HistoryQueryBuilder(not_serializable_input).process()
    #not_serializable_hist.pretty_print()

    #checks(not_serializable_hist)
    
if __name__== "__main__":
    main()
    
    # This is an example of randomly generating the history transaction
    #history_transactions = generate_transactions()
    #hist = History(history_transactions)
    #hist.randomize_schedule()
    #hist.pretty_print()