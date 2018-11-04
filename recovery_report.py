from recoverable_value import RecoverableValue

class RecoveryResult:
    def __init__(self, read_from_relationship):
        self.dep_op = read_from_relationship.dependent_operation
        self.read_from_op = read_from_relationship.read_from_operation
        self.dep_tx_complete_order = read_from_relationship.dep_tx_complete_order
        self.read_from_tx_complete_order = read_from_relationship.read_from_tx_complete_order
        self.recoverable_value = read_from_relationship.recoverable_value
        self.aca_value = read_from_relationship.aca_value
        self.strict_value = read_from_relationship.strict_value

    def get_recoverable_msg(self):
        return '{0} {1} {2} and T{3} {4} {5} T{6} {7}.'.format(
            self.dep_op.format_pretty(), 
            'overwrites' if self.dep_op.is_write() else 'reads from',
            self.read_from_op.format_pretty(),
            self.dep_op.transaction.id, 
            self.dep_op.transaction.commit_type().name.lower() + 's', 
            'before' if self.dep_tx_complete_order < self.read_from_tx_complete_order else 'after',
            self.read_from_op.transaction.id,
            self.read_from_op.transaction.commit_type().name.lower() + 's'
        )

    def get_strict_msg(self):
        return '{0} {1} {2} and T{3} {4} {5}.'.format(
            self.dep_op.format_pretty(), 
            'overwrites' if self.dep_op.is_write() else 'reads from',
            self.read_from_op.format_pretty(),
            self.read_from_op.transaction.id, 
            'commits' if self.strict_value is RecoverableValue.IS_STRICT else 'does not commit before',
            self.dep_op.format_pretty(), 
        )

    def get_aca_msg(self):
        return '{0} reads from {1} and T{2} {3} {4}.'.format(
            self.dep_op.format_pretty(), 
            self.read_from_op.format_pretty(),
            self.read_from_op.transaction.id, 
            'commits' if self.strict_value is RecoverableValue.IS_ACA else 'does not commit before',
            self.dep_op.format_pretty(), 
        )

class RecoveryReport:
    """RecoveryReport produces recovery results for a given history."""
    
    def __init__(self):
        # list of recovery results
        self.recovery_results = []

    def generate_strict_report(self):
        strict_report = "\n\n"
        
        if len(self.recovery_results) == 0:
            strict_report += 'Strict is not available for this history'
            return strict_report

        non_strict_results = [x for x in self.recovery_results if x.strict_value is RecoverableValue.IS_NOT_STRICT]
        is_strict_results = [x for x in self.recovery_results if x.strict_value is RecoverableValue.IS_STRICT]
        
        is_history_strict = len(non_strict_results) == 0
        result_list = is_strict_results if is_history_strict else non_strict_results

        strict_report += 'history is{0}strict because:'.format(' ' if is_history_strict else ' not ')

        for idx, result in enumerate(result_list):
            strict_report += '\n{0}) {1}'.format(idx+1, result.get_strict_msg())

        return strict_report

    def generate_aca_report(self):
        aca_report = "\n\n"
        
        if len(self.recovery_results) == 0:
            aca_report += 'ACA is not available for this history'
            return aca_report

        non_aca_results = [x for x in self.recovery_results if x.aca_value is RecoverableValue.IS_NOT_ACA]
        aca_results = [x for x in self.recovery_results if x.aca_value is RecoverableValue.IS_ACA]

        if (len(non_aca_results) + len(aca_results)) == 0:
            aca_report += 'ACA is not available for this history'
            return aca_report
        
        is_history_aca = len(non_aca_results) == 0
        result_list = aca_results if is_history_aca else non_aca_results

        aca_report += 'history is{0}ACA because:'.format(' ' if is_history_aca else ' not ')

        for idx, result in enumerate(result_list):
            aca_report += '\n{0}) {1}'.format(idx+1, result.get_aca_msg())

        return aca_report
    
    def generate_recoverable_report(self):
        recoverable_report = "\n"
        
        if len(self.recovery_results) == 0:
            recoverable_report += 'history is recoverable because there do not exist any read-from relationships.'
            return recoverable_report

        non_recoverable_results = [x for x in self.recovery_results if x.recoverable_value is RecoverableValue.IS_NOT_RECOVERABLE]
        recoverable_results = [x for x in self.recovery_results if x.recoverable_value is RecoverableValue.IS_RECOVERABLE]
        is_history_recoverable = len(non_recoverable_results) == 0
        result_list = recoverable_results if is_history_recoverable else non_recoverable_results

        recoverable_report += 'history is{0}recoverable because:'.format(' ' if is_history_recoverable else ' not ')

        for idx, result in enumerate(result_list):
            recoverable_report += '\n{0}) {1}'.format(idx+1, result.get_recoverable_msg())

        return recoverable_report

    def build_report(self, history):
        hist_title = history.format_pretty()
        report = '\nHistory Recovery Report\n{0}\n'.format(hist_title)
        

        report += "=" * len(hist_title)

        report += self.generate_recoverable_report()
        report += self.generate_aca_report()
        report += self.generate_strict_report()

        report += "\n" + "=" * len(hist_title) + "\n"
        
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
    
        
