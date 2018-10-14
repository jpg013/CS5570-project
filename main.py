from history import History
from token_processor import create_transactions_from_input
from recoverable_engine import RecoverableEngine

def main():
    input_str = "w1(x) r3(z) r2(x) c2 c1"

    token_result_set = create_transactions_from_input(input_str)
    hist = History()
    hist.set_transactions(token_result_set.transactions)
    hist.set_schedule(token_result_set.data_operations)
    hist.pretty_print()
    r_engine = RecoverableEngine(hist)
    r_engine.run()
    r_engine.pretty_print()

if __name__== "__main__":
    main()