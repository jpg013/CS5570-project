import networkx as nx
from history import History
from transaction import Transaction
from data_operation import DataOperation

def serializable_or_not(hist):
    conflicting_transactions = set()
    operations = hist.schedule

    for i in range(len(operations)):
        operation1=operations[i]
        for j in range(i+1,len(operations)):
            operation2=operations[j]
            id1 = operation1.transaction_id
            id2 = operation2.transaction_id
            if (id1 == id2 and
                (operation1.operation_type == "WRITE" or operation2.operation_type == "WRITE") and
                operation1.data_item == operation2.data_item):

                conflicting_transactions.add([id1,id2])

    l = list()
    for item in conflicting_transactions:
        l.add(item)

    G = nx.DiGraph(l)
    if find_cycle(G) != []:
        return False
    return True
