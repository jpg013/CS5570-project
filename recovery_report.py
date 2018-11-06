from recoverable_value import RecoverableValue

class RecoveryResult:
    """RecoveryResult Result"""
    
    def __init__(self, read_from_relationship):
        self.dep_op = read_from_relationship.dependent_operation
        self.read_from_op = read_from_relationship.read_from_operation
        self.dep_tx_complete_order = read_from_relationship.dep_tx_complete_order
        self.read_from_tx_complete_order = read_from_relationship.read_from_tx_complete_order
        self.recoverable_value = read_from_relationship.recoverable_value
        self.strict_value = read_from_relationship.strict_value
        self.aca_value = read_from_relationship.aca_value

    def get_recoverable_msg(self):
        if self.recoverable_value is RecoverableValue.NOT_AVAILABLE:
            return None
        
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
        if self.strict_value is RecoverableValue.NOT_AVAILABLE:
            return None
        
        return '{0} {1} {2} and T{3} {4} {5}.'.format(
            self.dep_op.format_pretty(), 
            'overwrites' if self.dep_op.is_write() else 'reads from',
            self.read_from_op.format_pretty(),
            self.read_from_op.transaction.id, 
            'commits before' if self.strict_value is RecoverableValue.IS_STRICT else 'does not commit before',
            self.dep_op.format_pretty(), 
        )

    def get_aca_msg(self):
        if self.aca_value is RecoverableValue.NOT_AVAILABLE:
            return None
        
        return '{0} reads from {1} and T{2} {3} {4}.'.format(
            self.dep_op.format_pretty(), 
            self.read_from_op.format_pretty(),
            self.read_from_op.transaction.id, 
            'commits' if self.strict_value is RecoverableValue.IS_ACA else 'does not commit before',
            self.dep_op.format_pretty(), 
        )

class RecoveryReport:
    """RecoveryReport produces recovery results for a given history."""
    
    def __init__(self, history, read_from_relationship_set):
        # list of recovery results
        self.recovery_results = []

        # holds the given history
        self.history = history

        # List of recoverable violations for the history
        self.recoverable_violations = []
        
        # List of recoverable violations for the history
        self.recoverable_compliances = []

        # List of aca violations for the history
        self.aca_violations = []

        # List of aca compliances for the history
        self.aca_compliances = []

        # List of strict violations for the history
        self.strict_violations = []

        # List of stict compliances for the history
        self.strict_compliances = []

        self.is_history_recoverable = None
        self.is_history_aca = None
        self.is_history_strict = None

        self.process_results(read_from_relationship_set)
        
    def generate_strict_report(self):
        strict_report = "\n\n"
        
        if self.is_history_strict is RecoverableValue.NOT_AVAILABLE:
            strict_report += 'Strict is not available for this history.'
        elif self.is_history_strict is RecoverableValue.IS_STRICT:
            strict_report += 'history is strict because:'

            for idx, result in enumerate(self.strict_compliances):
                strict_report += '\n{0}) {1}'.format(idx+1, result)
        else:
            strict_report += 'history is not strict because:'

            for idx, result in enumerate(self.strict_violations):
                strict_report += '\n{0}) {1}'.format(idx+1, result)

        return strict_report

    def generate_aca_report(self):
        aca_report = "\n\n"
        
        if self.is_history_aca is RecoverableValue.NOT_AVAILABLE:
            aca_report += 'ACA is not available for this history.'
        elif self.is_history_aca is RecoverableValue.IS_ACA:
            aca_report += 'history is aca because:'

            for idx, result in enumerate(self.aca_compliances):
                aca_report += '\n{0}) {1}'.format(idx+1, result)
        else:
            aca_report += 'history is not aca because:'

            for idx, result in enumerate(self.aca_violations):
                aca_report += '\n{0}) {1}'.format(idx+1, result)

        return aca_report
    
    def generate_recoverable_report(self):
        recoverable_report = "\n"
        
        if self.is_history_recoverable is RecoverableValue.NOT_AVAILABLE:
            recoverable_report += 'history is recoverable because there do not exist any read-from relationships.'
        elif self.is_history_recoverable is RecoverableValue.IS_RECOVERABLE:
            recoverable_report += 'history is recoverable because:'

            for idx, result in enumerate(self.recoverable_compliances):
                recoverable_report += '\n{0}) {1}'.format(idx+1, result)
        else:
            recoverable_report += 'history is not recoverable because:'

            for idx, result in enumerate(self.recoverable_violations):
                recoverable_report += '\n{0}) {1}'.format(idx+1, result)

        return recoverable_report

    def build_report(self):
        hist_title = self.history.format_pretty()
        report = '\nHistory Recovery Report\n{0}\n'.format(hist_title)

        report += "=" * len(hist_title)

        report += self.generate_recoverable_report()
        report += self.generate_aca_report()
        report += self.generate_strict_report()

        report += "\n" + "=" * len(hist_title) + "\n"
        
        self.report = report

    def display_pretty(self):
        print(self.report)

    def is_recoverable(self):
        return self.is_history_recoverable is not RecoverableValue.IS_NOT_RECOVERABLE

    def is_aca(self):
        return self.is_history_aca is not RecoverableValue.IS_NOT_ACA

    def is_strict(self):
        return self.is_history_strict is not RecoverableValue.IS_NOT_STRICT

    def process_results(self, read_from_relationship_set):
        for item in read_from_relationship_set:
            recovery_result = RecoveryResult(item)

            self.recovery_results.append(recovery_result)
            self.process_recoverable_result(recovery_result)
            self.process_aca_result(recovery_result) 
            self.process_strict_result(recovery_result)
        
        if len(self.recoverable_compliances) > 0 or len(self.recoverable_violations) > 0:
            self.is_history_recoverable = RecoverableValue.IS_RECOVERABLE if len(self.recoverable_violations) == 0 else RecoverableValue.IS_NOT_RECOVERABLE
        else:
            self.is_history_recoverable = RecoverableValue.NOT_AVAILABLE

        if len(self.aca_compliances) > 0 or len(self.aca_violations) > 0:
            self.is_history_aca = RecoverableValue.IS_ACA if len(self.aca_violations) == 0 else RecoverableValue.IS_NOT_ACA
        else:
            self.is_history_aca = RecoverableValue.NOT_AVAILABLE

        if len(self.strict_compliances) > 0 or len(self.strict_violations) > 0:
            self.is_history_strict = RecoverableValue.IS_STRICT if len(self.strict_violations) == 0 else RecoverableValue.IS_NOT_STRICT
        else:
            self.is_history_strict = RecoverableValue.NOT_AVAILABLE
        
    def process_recoverable_result(self, recovery_result):
        msg = recovery_result.get_recoverable_msg()

        if msg is None:
            return

        if recovery_result.recoverable_value is RecoverableValue.IS_RECOVERABLE:
            self.recoverable_compliances.append(msg)
        else:
            self.recoverable_violations.append(msg)

    def process_strict_result(self, recovery_result):
        msg = recovery_result.get_strict_msg()

        if msg is None:
            return

        if recovery_result.strict_value is RecoverableValue.IS_STRICT:
            self.strict_compliances.append(msg)
        else:
            self.strict_violations.append(msg)

    def process_aca_result(self, recovery_result):
        msg = recovery_result.get_aca_msg()

        if msg is None:
            return

        if recovery_result.aca_value is RecoverableValue.IS_ACA:
            self.aca_compliances.append(msg)
        else:
            self.aca_violations.append(msg)
    
        
