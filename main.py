from history import History
from serializable_engine import SerializableEngine
from token_processor import create_transactions_from_input
from recoverable_engine import RecoverableEngine

def main():
    input_str = "w1(x) r2(x) c2 c1"

    token_result_set = create_transactions_from_input(input_str)
    hist = History()
    hist.set_transactions(token_result_set[0])
    hist.set_schedule(token_result_set[1])
    hist.pretty_print()
    
    s_engine = SerializableEngine(hist)
    s_engine.run()

    r_engine = RecoverableEngine(hist)
    r_engine.run()

if __name__== "__main__":
    main()