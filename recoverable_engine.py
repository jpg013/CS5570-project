from data_operation import OperationType
import collections

read_set_result = collections.namedtuple('ReadSetResult', ['read_op', 'write_op'])

class RecoverableEngine:
    """RecoverableEngine class. Given a history will determine whether or not
    the history is recoverable, avoids cascading aborts (aca), and is strict."""

    def __init__(self, history):
        if history is None:
            raise ValueError("History must be defined.")
      
        self.history = history
        self.read_set = set()

        # a list containing the order that each transaction in the history either commits/aborts. List items
        # are tranasction_ids, and the index of the item signifies the order. So [1, 2] implies T1 commits/aborts 
        # before T2 commits/aborts
        self.tx_commit_abort_order = []

        # set containing read_set recoverability infractions, read/write pairs that are not recoverable.
        self.recoverability_infractions = set()
  
    def run(self):
        #self.build_node_edges()
        self.construct_read_set()
        self.determine_transaction_terminate_order()
        self.determine_recoverability()
        print(len(self.recoverability_infractions))

    def determine_recoverability(self):
        """To determine recoverability, for each graph node edge T1 -> T2, where T1 read from T2,
        c2 < c1 or a1 < a2."""
        
        for item in self.read_set:
            read_op  = item.read_op
            write_op = item.write_op

            tx_a = self.history.get_transaction_by_id(read_op.transaction_id)
            tx_b = self.history.get_transaction_by_id(write_op.transaction_id)

            is_recoverable = self.is_transaction_recoverable(tx_a, tx_b)

            # Add unrecoverable node tuples to a set
            if not is_recoverable:
                self.recoverability_infractions.add(item)

    def display_recoverable_error_message(self, read_set_result):
        read_op = read_set_result.read_op
        write_op = read_set_result.write_op

        read_tx = self.history.get_transaction_by_id(read_op.transaction_id)
        write_tx = self.history.get_transaction_by_id(write_op.transaction_id)
        
        read_formatted_commit_type = read_tx.commit_type().name.lower() + 's'
        write_formatted_commit_type = write_tx.commit_type().name.lower() + 's'

        print('history is not recoverable because T{0} reads from T{1} and T{0} {2} before T{1} {3}.'
            .format(read_tx.transaction_id, write_tx.transaction_id, read_formatted_commit_type, write_formatted_commit_type))

    def is_transaction_recoverable(self, tx_a, tx_b):
        """tx_a is dependent on / reads from tx_b"""
        a_order = self.tx_commit_abort_order.index(tx_a.transaction_id)
        b_order = self.tx_commit_abort_order.index(tx_b.transaction_id)

        # some ugly use cases here.
        if tx_a.commit_type() is OperationType.COMMIT and tx_b.commit_type() is OperationType.COMMIT:
            # case1: a && b both commit, since a reads from b, b must commit first
            return b_order < a_order

        if tx_a.commit_type() is OperationType.ABORT and tx_b.commit_type() is OperationType.COMMIT:
            # case2: a aborts while b commits, for this to be recoverable tx_a must abort after tx_b commits
            return b_order < a_order

        if tx_a.commit_type() is OperationType.COMMIT and tx_b.commit_type() is OperationType.ABORT:
            # case3: a commits while b aborts, for this to be recoverable tx_a must abort before tx_b commits
            return a_order < b_order

        if tx_a.commit_type() is OperationType.ABORT and tx_b.commit_type() is OperationType.ABORT:
            # case3: a and b both abort, then a must abort before b 
            return a_order < b_order

        # we should never reach this case?
        raise Exception('what the hell!')

    def determine_transaction_terminate_order(self):
        for item in self.history.schedule:
            if item.is_abort() or item.is_commit():
                self.tx_commit_abort_order.append(item.transaction_id)
    
    def construct_read_set(self):
        """Find edge relationships between nodes. We say a node Ti, reads x from Tj in history H if:
        1) wj(x) < ri(x)
        2) aj !< ri(x)
        3) if there is some wk(x) such that wj(x) < wk(x) < ri(x), then ak < ri(x)
        """

        schedule = self.history.schedule[0:]

        for idx, read_op in enumerate(schedule):
            # cannot read from previous data if first element
            if idx == 0:
                continue

            # must be a read operation
            if not read_op.is_read():
                continue
            
            # look for an write to the same data item
            r_slice = schedule[0:idx]
            write_found = None

            for write_op in reversed(r_slice):
                # only care about same data item write op
                if write_op.data_item != read_op.data_item:
                    continue
                
                # Filter out non-writes
                if not write_op.is_write():
                    continue

                # break if same transaction
                if write_op.transaction_id != read_op.transaction_id:
                    write_found = write_op
                
                break

            if write_found is None:
                continue
            
            start_idx = schedule.index(write_found) + 1

            if start_idx >= idx:
                raise Exception('invalid index bounds')
                
            # Check for aborts in the index slice
            abort_exists = any(item.is_abort() and item.transaction_id == write_found.transaction_id for item in schedule[start_idx:idx])

            # An abort exists, so read_op does not read from write_op
            if abort_exists:
                print('found abort!!!')
                continue
            
            # There is a read from relation. Add a tuple to the read set
            self.read_set.add(read_set_result(read_op, write_op))
    
    def pretty_print(self):
        for item in self.recoverability_infractions:
            self.display_recoverable_error_message(item)


                

                      
        


        
                

    

  
    

