"""
dependent_operation = func_dep.dependent_operation
read_from_operation = func_dep.read_from_operation

dep_tx       = func_dep.dependent_operation.transaction
read_from_tx = func_dep.read_from_operation.transaction

dep_formatted_commit_type = dep_tx.commit_type().name.lower() + 's'
read_from_formatted_commit_type = read_from_tx.commit_type().name.lower() + 's'

formatted_order = 'before' if self.tx_completed_order[dep_tx.id] < self.tx_completed_order[read_from_tx.id] else 'after'
formatted_dep_op_type = dependent_operation.operation_type.name.lower() + 's'

msg = '{0} {1} from {2} and '.format(dependent_operation.format_pretty(), formatted_dep_op_type, read_from_operation.format_pretty())

msg = msg + 'T{0} {1} {2} '.format(dep_tx.id, dep_formatted_commit_type, formatted_order)

msg = msg + 'T{0} {1}.'.format(read_from_tx.id, read_from_formatted_commit_type)

self.recovery_compliances.append(msg) if func_dep.is_recoverable else self.recovery_violations.append(msg)
"""

class RecoveryResult:
    def __init__(self, read_from_relationship):
        self.dep_op = read_from_relationship.dependent_operation
        self.read_from_op = read_from_relationship.read_from_operation
        self.dep_tx_complete_order = read_from_relationship.dep_tx_complete_order
        self.read_from_tx_complete_order = read_from_relationship.read_from_tx_complete_order
        self.is_recoverable = read_from_relationship.is_recoverable
        self.is_aca = read_from_relationship.is_aca
        self.is_strict = read_from_relationship.is_strict

    def get_recoverable_msg(self):
        formatted_order = 'before' if self.dep_tx_complete_order < self.read_from_tx_complete_order else 'after'

        msg = '{0} {1} {2} and '.format(
            self.dep_op.format_pretty(), 
            'overwrites' if self.dep_op.is_write() else 'reads from',
            self.read_from_op.format_pretty()
        )

        msg += 'T{0} {1} {2} '.format(self.dep_op.transaction.id, self.dep_op.transaction.commit_type().name.lower() + 's', formatted_order)

        msg += 'T{0} {1}.'.format(self.read_from_op.transaction.id, self.read_from_op.transaction.commit_type().name.lower() + 's')

        return msg

class RecoveryReport:
    """RecoveryReport produces recovery results for a given history."""
    
    def __init__(self):
        # list of recovery results
        self.recovery_results = []

    def generate_strict_report(self):
        is_history_strict = len(self.strict_violations) == 0

        report = 'history is{0}strict because:'.format(' ' if is_history_strict else ' not ')

        reasons = self.strict_compliances[0:] if is_history_strict else self.strict_violations[0:]

        for idx, reason in enumerate(reasons):
            report = report + '\n{0}) {1}'.format(idx+1, reason)

        return report

    def generate_aca_report(self):
        aca_report = "\n\n"
        
        if len(self.recovery_results) == 0:
            aca_report += 'ACA is not available for this history'
            return aca_report

        non_aca_results = [x for x in self.recovery_results if x.is_aca == False]
        aca_results = [x for x in self.recovery_results if x.is_aca == True]
        
        if len(non_aca_results) + len(aca_results):
            aca_report += 'ACA is not available for this history'
            return aca_report
        
        is_history_aca = len(non_aca_results) == 0
        result_list = aca_results if is_history_aca else non_aca_results

        aca_report += 'history is{0}ACA because:'.format(' ' if is_history_aca else ' not ')

        for idx, result in enumerate(result_list):
            aca_report += '\n{0}) {1}'.format(idx+1, result.get_aca_msg())

        return aca_report
    
    def generate_recoverable_report(self):
        recoverable_report = "\n\n"
        
        if len(self.recovery_results) == 0:
            recoverable_report += 'history is recoverable because there do not exist any read-from relationships.'
            return recoverable_report

        non_recoverable_results = [x for x in self.recovery_results if x.is_recoverable == False]
        recoverable_results = [x for x in self.recovery_results if x.is_recoverable == True]
        is_history_recoverable = len(non_recoverable_results) == 0
        result_list = recoverable_results if is_history_recoverable else non_recoverable_results

        recoverable_report += 'history is{0}recoverable because:'.format(' ' if is_history_recoverable else ' not ')

        for idx, result in enumerate(result_list):
            recoverable_report += '\n{0}) {1}'.format(idx+1, result.get_recoverable_msg())

        return recoverable_report

    def build_report(self, history):
        report = 'Recovery Report for history: {0}\n'.format(history.format_pretty())

        report += "=" * len(report)

        report += self.generate_recoverable_report()
        report += self.generate_aca_report()
        
        return report

    def process_result(self, read_from_relationship=None):
        if read_from_relationship is None:
            raise Exception('read_from_relationship must be defined')

        recovery_result = RecoveryResult(read_from_relationship)

        self.recovery_results.append(recovery_result)

    def process_strict_result(self, func_dep=None):
        if func_dep is None:
            raise Exception('func_dep must be defined')

        self.build_strict_result(func_dep)
        
    def build_recovery_result(self, read_from_relationship):
        dependent_operation = func_dep.dependent_operation
        read_from_operation = func_dep.read_from_operation
        
        dep_tx       = func_dep.dependent_operation.transaction
        read_from_tx = func_dep.read_from_operation.transaction
        
        dep_formatted_commit_type = dep_tx.commit_type().name.lower() + 's'
        read_from_formatted_commit_type = read_from_tx.commit_type().name.lower() + 's'

        formatted_order = 'before' if self.tx_completed_order[dep_tx.id] < self.tx_completed_order[read_from_tx.id] else 'after'
        formatted_dep_op_type = dependent_operation.operation_type.name.lower() + 's'

        msg = '{0} {1} from {2} and '.format(dependent_operation.format_pretty(), formatted_dep_op_type, read_from_operation.format_pretty())

        msg = msg + 'T{0} {1} {2} '.format(dep_tx.id, dep_formatted_commit_type, formatted_order)

        msg = msg + 'T{0} {1}.'.format(read_from_tx.id, read_from_formatted_commit_type)
        
        self.recovery_compliances.append(msg) if func_dep.is_recoverable else self.recovery_violations.append(msg)
        
    def build_aca_result(self, func_dep):
        if func_dep is None:
            raise Exception('func_dep must be defined')

        write_tx = func_dep.write_op.transaction

        formatted_dep_op_type = func_dep.dep_op.operation_type.name.lower() + 's'

        msg = '{0} {1} from {2} and '.format(func_dep.dep_op.format_pretty(), formatted_dep_op_type, func_dep.write_op.format_pretty())
        
        if func_dep.is_aca:
            msg = msg + 'T{0} commits before {1}.'.format(write_tx.id, func_dep.dep_op.format_pretty())
        else:
            msg = msg + 'T{0} does not commit before {1}.'.format(write_tx.id, func_dep.dep_op.format_pretty())

        self.aca_compliances.append(msg) if func_dep.is_aca else self.aca_violations.append(msg)

    def build_strict_result(self, func_dep):
        if func_dep is None:
            raise Exception('func_dep must be defined')
            
        write_tx = func_dep.write_op.transaction

        formatted_dep_op_type = func_dep.dep_op.operation_type.name.lower() + 's'

        msg = '{0} {1} from {2} and '.format(func_dep.dep_op.format_pretty(), formatted_dep_op_type, func_dep.write_op.format_pretty())

        if func_dep.is_strict:
            msg = msg + 'T{0} commits before {1}.'.format(write_tx.id, func_dep.dep_op.format_pretty())
        else:
            msg = msg + 'T{0} does not commit before {1}.'.format(write_tx.id, func_dep.dep_op.format_pretty())

        self.strict_compliances.append(msg) if func_dep.is_strict else self.strict_violations.append(msg)
                    

        
