from history import History
from serializable_engine import SerializableEngine

def main():
  hist = History();
  hist.pretty_print()
  SerializableEngine(hist)

if __name__== "__main__":
  main()