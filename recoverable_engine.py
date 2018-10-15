from data_operation import OperationType
import collections

read_set_result = collections.namedtuple('ReadSetResult', ['read_op', 'write_op'])

class IsRecoverableResult:
    def __init__(self, violations):
        self.violations = violations
        self.is_recoverable = len(self.violations) == 0
        self.message = self.format_message()

    def format_message(self):
        if self.is_recoverable:
            return 'history is recoverable.'

        base_message = 'history is not recoverable because '

        for idx, v in enumerate(self.violations):
            read_tx = v[0]
            write_tx = v[1]
            
            read_formatted_commit_type = read_tx.commit_type().name.lower() + 's'
            write_formatted_commit_type = write_tx.commit_type().name.lower() + 's'

            msg = ''

            if idx > 0:
                msg = msg + ' and '

            msg = 'T{0} reads from T{1} and T{0} {2} before T{1} {3}'.format(read_tx.transaction_id, write_tx.transaction_id, read_formatted_commit_type, write_formatted_commit_type)
            
            base_message = base_message + msg

            if idx >= (len(self.violations) - 1):
                base_message = base_message + '.'

        return base_message

class ACAResult:
    def __init__(self, violations):
        self.violations = violations
        self.is_aca = len(self.violations) == 0
        self.message = self.format_message()

    def format_message(self):
        if self.is_aca:
            return 'history is aca.'

        base_message = 'history is not aca because '

        for idx, v in enumerate(self.violations):
            read_tx = v[0]
            write_tx = v[1]
            
            msg = ''

            if idx > 0:
                msg = msg + ' and '

            msg = 'T{0} reads from T{1} before T{1} commits it data operations'.format(read_tx.transaction_id, write_tx.transaction_id)
            
            base_message = base_message + msg

            if idx >= (len(self.violations) - 1):
                base_message = base_message + '.'

        return base_message

class RecoverableEngine:
    """RecoverableEngine class. Given a history will determine whether or not
    the history is recoverable, avoids cascading aborts (aca), and is strict."""

    def __init__(self, history):
        if history is None:
            raise ValueError("History must be defined.")
      
        self.history = history
        # set of read/write tuples where read op reads data from write op for data item
        self.read_set = set()

        # a list containing the order that each transaction in the history either commits/aborts. List items
        # are tranasction_ids, and the index of the item signifies the order. So [1, 2] implies T1 commits/aborts 
        # before T2 commits/aborts
        self.tx_commit_abort_order = []

        self.construct_read_set()
        self.build_transaction_commit_abort_order()


    def is_aca(self):
        """To determine aca, if T1 reads from T2, the T2 must commit before any operation in T1 reads data that is 
        written by T2. Returns a tuple where first value is a bool indicating recoverability, the 
        second value is the set of recoverable violations. It will be empty if history is recoverable."""

        violations = set()
        schedule = self.history.schedule[0:]

        for item in self.read_set:
            read_op  = item.read_op
            write_op = item.write_op

            read_tx = self.history.get_transaction_by_id(read_op.transaction_id)
            write_tx = self.history.get_transaction_by_id(write_op.transaction_id)

            start_idx = schedule.index(write_op)
            end_idx = schedule.index(read_op)
            new_slice = schedule[start_idx: end_idx]

            commit_found = any(x.is_commit() and x.transaction_id == write_op.transaction_id for x in schedule[start_idx:end_idx])
            
            # check if violates aca
            if not commit_found:
                violations.add((read_tx, write_tx))

        return ACAResult(violations)
        
    def is_recoverable(self):
        """To determine recoverability, for each graph node edge T1 -> T2, where T1 read from T2,
        c2 < c1 or a1 < a2. Returns a tuple where first value is a bool indicating recoverability, the 
        second value is the set of recoverable violations. It will be empty if history is recoverable."""

        # set containing read_set recoverability violations, read/write pairs that are not recoverable.
        violations = set()
        
        for item in self.read_set:
            read_op  = item.read_op
            write_op = item.write_op

            read_tx = self.history.get_transaction_by_id(read_op.transaction_id)
            write_tx = self.history.get_transaction_by_id(write_op.transaction_id)

            pair_recoverable = self.determine_tx_pair_recoverability(read_tx, write_tx)

            # Add unrecoverable node tuples to a set
            if not pair_recoverable:
                violations.add((read_tx, write_tx))
        
        return IsRecoverableResult(violations)

    def format_recoverable_error_message(self, read_set_result):
        read_op = read_set_result.read_op
        write_op = read_set_result.write_op

        read_tx = self.history.get_transaction_by_id(read_op.transaction_id)
        write_tx = self.history.get_transaction_by_id(write_op.transaction_id)
        
        read_formatted_commit_type = read_tx.commit_type().name.lower() + 's'
        write_formatted_commit_type = write_tx.commit_type().name.lower() + 's'

        print('history is not recoverable because T{0} reads from T{1} and T{0} {2} before T{1} {3}.'
            .format(read_tx.transaction_id, write_tx.transaction_id, read_formatted_commit_type, write_formatted_commit_type))

    def determine_tx_pair_recoverability(self, tx_a, tx_b):
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

    def build_transaction_commit_abort_order(self):
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
            
            start_idx = schedule.index(write_found)

            if start_idx >= idx:
                raise Exception('invalid index bounds')
                
            # Check for aborts in the index slice
            abort_exists = any(item.is_abort() and item.transaction_id == write_found.transaction_id for item in schedule[start_idx:idx])

            # An abort exists, so read_op does not read from write_op
            if abort_exists:
                continue
            
            # There is a read from relation. Add a tuple to the read set
            self.read_set.add(read_set_result(read_op, write_op))

                

                      
        


        
                

    

  
    

