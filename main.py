from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import generate_transactions
from recovery_engine import RecoveryEngine

def main():
    not_recoverable_hist_input = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] c2 w1[z] c1'
    not_recoverable_hist = HistoryQueryBuilder(not_recoverable_hist_input).process()
    not_recoverable_hist.pretty_print()

    recovery_engine = RecoveryEngine(not_recoverable_hist)
    results = recovery_engine.analyze()
    print(results.get_report())

    print('\n', end="")
    
    recoverable_not_aca_input = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] w1[z] c1 c2'
    recoverable_not_aca_hist = HistoryQueryBuilder(recoverable_not_aca_input).process()
    recoverable_not_aca_hist.pretty_print()

    recovery_engine = RecoveryEngine(recoverable_not_aca_hist)
    results = recovery_engine.analyze()
    print(results.get_report())

    print('\n', end="")

    aca_not_strict_input = 'w1[x] w1[y] r2[u] w2[x] w1[z] c1 r2[y] w2[y] c2'
    aca_not_strict_hist = HistoryQueryBuilder(aca_not_strict_input).process()
    aca_not_strict_hist.pretty_print()

    recovery_engine = RecoveryEngine(aca_not_strict_hist)
    results = recovery_engine.analyze()
    print(results.get_report())

    #hist = History()
    #hist.add_transactions(generate_transactions()).randomize_schedule()
    #hist.pretty_print()
    
    
if __name__== "__main__":
    main()