from history import History
from serializable_engine import SerializableEngine

def main():
    hist = History()
    hist.pretty_print()

    engine = SerializableEngine(hist)

    engine.run()

if __name__== "__main__":
    main()