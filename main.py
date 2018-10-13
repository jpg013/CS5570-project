from history import History
from serializable_engine import SerializableEngine
from token_processor import create_transactions_from_input

def main():
    input_str = "w1(x) w2(x) w3(x) w1(x) c1 c2 c3"

    token_result_set = create_transactions_from_input(input_str)
    hist = History()
    hist.set_transactions(token_result_set[0])
    hist.set_schedule(token_result_set[1])
    hist.pretty_print()
    #hist.make_schedule()
    #hist.generate_transactions()
    # hist.make_schedule()

    engine = SerializableEngine(hist)
    engine.run()

if __name__== "__main__":
    main()