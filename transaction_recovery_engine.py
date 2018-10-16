from data_operation import OperationType
import collections

read_from_result = collections.namedtuple('ReadSetResult', ['read_op', 'write_op'])

class ReadFromRelationship:
    """ReadRecoverResult analyzes two transactions (tx_a and tx_b) where tx_a reads
    a data item from tx_b. It analyzes whether or not tx_a is recoverable by 
    analyzing the commit/abort order of the transactions and the rules thereby."""

    def __init__(self, read_op, write_op):
        if read_op is None or write_op is None:
            raise Exception('read/write op must be defined')

        #if not isinstance(read_tx_order, int) or not isinstance(write_tx_order, int):
            #raise Exception('read/write order must be an int')

        self.read_op = read_op
        self.write_op = write_op
        self.is_recoverable = False # default recoverable to false
        self.is_aca = False # defualt aca to false
        self.recoverable_message = ''
        self.aca_message = ''

    def format_recovery_message(self):
        #message = 'history is{0}recoverable because T{1} reads from T{2} and : '
         #   .format(' ' if self.is_recoverable else ' not ', self.tx_a.id, self.tx_b.id)

        read_op_commit_type = self.read_op.transaction.commit_type().name.lower() + 's'
        write_op_commit_type = self.write_op.transaction.commit_type().name.lower() + 's'

        for idx, v in enumerate(recover_violations):
            read_tx = v[0]
            write_tx = v[1]
            
            read_formatted_commit_type = read_tx.commit_type().name.lower() + 's'
            write_formatted_commit_type = write_tx.commit_type().name.lower() + 's'

            msg = ''

            if idx > 0:
                msg = msg + ' and '

            msg = 'T{0} reads from T{1} and T{0} {2} before T{1} {3}'.format(read_tx.transaction_id, write_tx.transaction_id, read_formatted_commit_type, write_formatted_commit_type)
            
            base_message = base_message + msg

            if idx >= (len(recover_violations) - 1):
                base_message = base_message + '.'

        return base_message

class TransactionRecoveryResult:
    def __init__(self, recovery_result, aca_result):
        self.recovery_result = recovery_result
        self.aca_result = aca_result
        
        
    def format_aca_message(self):
        if self.is_aca:
            return 'history is aca.'

        base_message = 'history is not aca because '

        for idx, v in enumerate(self.aca_violations):
            read_tx = v[0]
            write_tx = v[1]
            
            msg = ''

            if idx > 0:
                msg = msg + ' and '

            msg = 'T{0} reads from T{1} before T{1} commits it data operations'.format(read_tx.transaction_id, write_tx.transaction_id)
            
            base_message = base_message + msg

            if idx >= (len(self.aca_violations) - 1):
                base_message = base_message + '.'

        return base_message
    
    def format_recovery_message(self):
        if self.is_recoverable:
            return 'history is recoverable.'

        base_message = 'history is not recoverable because '

        for idx, v in enumerate(self.recover_violations):
            read_tx = v[0]
            write_tx = v[1]
            
            read_formatted_commit_type = read_tx.commit_type().name.lower() + 's'
            write_formatted_commit_type = write_tx.commit_type().name.lower() + 's'

            msg = ''

            if idx > 0:
                msg = msg + ' and '

            msg = 'T{0} reads from T{1} and T{0} {2} before T{1} {3}'.format(read_tx.transaction_id, write_tx.transaction_id, read_formatted_commit_type, write_formatted_commit_type)
            
            base_message = base_message + msg

            if idx >= (len(self.recover_violations) - 1):
                base_message = base_message + '.'

        return base_message


class TransactionRecoveryEngine:
    """TransactionRecoveryEngine class. Given a history will determine whether or not
    the history is recoverable, avoids cascading aborts (aca), and is strict."""

    def __init__(self, history):
        if history is None:
            raise ValueError("History must be defined.")
      
        self.history = history
        # set of ReadRecoveryResults containing a read op that reads data item written by write op from a 
        # different transaction
        
        self.read_from_set = set()

        # a dict containing the order that each transaction in the history either commits/aborts. The keys are 
        # transaction ids, and the value is the order of completion, starting at index 1.
        #
        self.tx_completed_order = {}

        # set of violations for recovery
        #self.recovery_violations = set()

        # set of violations for aca
        #self.aca_violations = set()
        
    def analyze(self):
        """Main method to be called to analyze the history. Returns a RecoveryResult"""
        
        # Determine the order in which the transactions completed. This is needed for recoverability
        self.determine_tx_completed_order()
        
        # Construct the set of read from relationships
        self.construct_read_from_set()

        # Construct the set of read from relationships
        self.process_read_from_set()

        return self.build_results()

    def build_results(self):
        
        
    def process_read_from_set(self):
        """Iterates over each read set item and computes recoverable/aca properties."""
        for item in self.read_from_set:
            item.is_recoverable = self.determine_recoverable(item.read_op, item.write_op)            
            item.is_aca = self.determine_aca(item.read_op, item.write_op)
            
    def determine_recoverable(self, read_op, write_op):
        """Rules for determining whether read_tx is recoverable with regards to write_tx. Returns True is recoverable else False"""
        
        read_tx = read_op.transaction
        write_tx = write_op.transaction
        
        read_tx_complete_order = self.tx_completed_order[read_tx.id]
        write_tx_complete_order = self.tx_completed_order[write_tx.id]

        # some ugly use cases here.
        if read_tx.commit_type() is OperationType.COMMIT and write_tx.commit_type() is OperationType.COMMIT:
            # case1: read_tx && write_tx both commit, since read_tx reads from write_tx, write_tx must commit first
            return write_tx_complete_order < read_tx_complete_order

        if read_tx.commit_type() is OperationType.ABORT and write_tx.commit_type() is OperationType.COMMIT:
            # case2: read_tx aborts while write_tx commits, for this to be recoverable read_tx must abort after write_tx commits
            return write_tx_complete_order < read_tx_complete_order

        if read_tx.commit_type() is OperationType.COMMIT and write_tx.commit_type() is OperationType.ABORT:
            # case3: read_tx commits while write_tx aborts, for this to be recoverable read_tx must abort before write_tx commits
            return read_tx_complete_order < write_tx_complete_order

        if read_tx.commit_type() is OperationType.ABORT and write_tx.commit_type() is OperationType.ABORT:
            # case3: read_tx and write_tx both abort, then read_tx must abort before read_tx
            return read_tx_complete_order < write_tx_complete_order

        # we should never reach this case?
        raise Exception('what the hell!')

    def determine_aca(self, read_op, write_op):
        """To determine aca we follow the logic that if T1 reads from T2, the T2 must commit 
        before any operation in T1 reads data that is written by T2. Returns True is aca else false."""

        return self.find_commit_between_operations(read_op, write_op)

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

    def determine_tx_completed_order(self):
        order = 1
        for data_op in self.history.schedule:
            if data_op.is_abort() or data_op.is_commit():
                self.tx_completed_order[data_op.transaction.id] = order
                order += 1

    def find_commit_between_operations(self, read_op=None, write_op=None):
        start_idx = self.history.schedule.index(write_op)
        end_idx = self.history.schedule.index(read_op)
        sched_slice = self.history.schedule[start_idx:end_idx]

        if start_idx >= end_idx:
            raise Exception('invalid index bounds')

        return any(op.is_commit() and op.transaction is write_op.transaction for op in sched_slice)
    
    def find_abort_between_operations(self, read_op=None, write_op=None):
        start_idx = self.history.schedule.index(write_op)
        end_idx = self.history.schedule.index(read_op)
        schedule_slice = self.history.schedule[start_idx:end_idx]

        if start_idx >= end_idx:
            raise Exception('invalid index bounds')
                
        # Check for aborts in the index slice
        return any(item.is_abort() and item.transaction is write_op.transaction for item in schedule_slice)

    def add_read_from_set_item(self, read_op, write_op):
        self.read_from_set.add(ReadFromRelationship(read_op, write_op))
        
    def construct_read_from_set(self):
        """Find edge relationships between nodes. We say a node Ti, reads x from Tj in history H if:
        1) wj(x) < ri(x)
        2) aj !< ri(x)
        3) if there is some wk(x) such that wj(x) < wk(x) < ri(x), then ak < ri(x)
        """
        # init the read_from_set
        self.read_from_set = set()
        
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
                if write_op.transaction is read_op.transaction:
                    break
                
                write_found = write_op
                break

            if write_found is None:
                continue
            
            abort_exists = self.find_abort_between_operations(read_op, write_found)
            
            # An abort exists, so read_op does not read from write_op
            if abort_exists:
                continue
            
            # There is a read from relation. Add a tuple to the read set
            self.add_read_from_set_item(read_op, write_op)
            

                

                      
        


        
                

    

  
    

