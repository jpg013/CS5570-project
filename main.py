from history import History
from serializable_engine import SerializableEngine
from token_processor import create_transactions_from_input

def main():
    input_str = "r1(x) w1(x) c1"

    transactions = create_transactions_from_input(input_str)

    hist = History()
    hist.set_transactions(transactions)
    hist.make_schedule()

    # hist.generate_transactions()
    # hist.make_schedule()
    hist.pretty_print()

    engine = SerializableEngine(hist)
    engine.run()

if __name__== "__main__":
    main()