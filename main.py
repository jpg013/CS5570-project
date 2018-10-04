from history import History
from transaction import OperationType

def main():
  hist = History()
  
  for item in hist.complete_history:
    if item == hist.complete_history[-1]:
      print(item.pretty_format())
    else:
      print(item.pretty_format(), end=" --> ")


if __name__== "__main__":
  main()

#test
