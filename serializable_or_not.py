import networkx as nx
from history import History
from transaction import Transaction
from data_operation import DataOperation
from history_query_builder import HistoryQueryBuilder

def serializable_or_not(hist):
    conflicting_transactions = set()
    operations = hist.schedule
    
    for i in range(len(operations)):
        operation1=operations[i]
        for j in range(i+1,len(operations)):
            operation2=operations[j]
            id1 = operation1.transaction.id
            id2 = operation2.transaction.id
            if (id1 != id2 and
                (operation1.is_write() or operation2.is_write()) and
                operation1.data_item == operation2.data_item and
                not operation1.is_commit() and not operation2.is_commit() and
                not operation1.is_abort() and not operation2.is_abort()):
                
                conflicting_transactions.add((id1,id2))

    l = list()
    for item in conflicting_transactions:
        l.append(item)
    

    G = nx.DiGraph(l)
    try:
        l = list(nx.find_cycle(G)) #raises an exception if a cycle is NOT found
        cycle = True                  #if it makes it to this line, then there is a cycle
    except:                           #i don't know if this is bad practice or not, but that's how this nx.find_cycle() function works.
        cycle = False
    #print(l)
    return not cycle                  #return the opposite if we found a cycle (serializable if cycle == false

"""
def test_serializable():
    serial_input = "w1[x] r3[z] r2[x] c2 c1"
    not_serial_input = "w1[x] w2[x] w2[y] c2 w1[y] w3[x] w3[y] c3 c1"
    
    serializable_hist = HistoryQueryBuilder(serial_input).process()
    not_serializable_hist = HistoryQueryBuilder(not_serial_input).process()

    serial_res = serializable_or_not(serializable_hist)
    print(serial_res)
    print ("\n\n")
    not_serial_res = serializable_or_not(not_serializable_hist)
    print(not_serial_res)
    print("\n\n")
    
    return serial_res and not not_serial_res
    

test = test_serializable()
if(test):
    print("pass")
else:
    print("fail")
"""
