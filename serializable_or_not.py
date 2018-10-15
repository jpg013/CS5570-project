import networkx as nx
from history import History
from transaction import Transaction
from data_operation import DataOperation
from token_processor import create_transactions_from_input

def serializable_or_not(hist):
    hist.pretty_print()
    conflicting_transactions = set()
    operations = hist.schedule
    
    for i in range(len(operations)):
        operation1=operations[i]
        for j in range(i+1,len(operations)):
            operation2=operations[j]
            id1 = operation1.transaction_id
            id2 = operation2.transaction_id
            if (id1 != id2 and
                (str(operation1.operation_type) == "OperationType.WRITE" or str(operation2.operation_type) == "OperationType.WRITE") and
                operation1.data_item == operation2.data_item and
                (operation1.data_item != None) and (operation2.data_item != None)):
                
                conflicting_transactions.add((id1,id2))

    l = list()
    for item in conflicting_transactions:
        l.append(item)
    

    G = nx.DiGraph(l)
    try:
        print(list(nx.find_cycle(G))) #raises an exception if a cycle is NOT found
        cycle = True                  #if it makes it to this line, then there is a cycle
    except:                           #i don't know if this is bad practice or not, but that's how this nx.find_cycle() function works.
        cycle = False
    return cycle

def test_serializable():
    #just comment out whichever one you don't want
    input_str = "w1(x) r3(z) r2(x) c2 c1"
    #input_str = "w1(x) w2(x) w2(y) c2 w1(y) w3(x) w3(y) c3 c1"
    token_result_set = create_transactions_from_input(input_str)
    
    hist = History()
    hist.set_transactions(token_result_set.transactions)
    hist.set_schedule(token_result_set.data_operations)
    hist.pretty_print()
    return serializable_or_not(hist)

test = test_serializable()
if(test):
    print("true")
else:
    print("false")
    
