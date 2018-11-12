from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import DataGeneration
from recovery_engine import RecoveryEngine
from serializable_or_not import serializable_or_not
from app_config import AppConfig

def build_graphs():
    data_graph = build_data_graph()
    tx_graph = build_transaction_graph()
    
    return {
        'transaction_graph': tx_graph,
        'data_set_graph': data_graph
    }

def build_data_graph():
    iter_count = 100
    results = []
    data_items = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    
    for idx in range(10):
        AppConfig.set('data_set', set(data_items[0:idx+1]))

        not_recoverable_count = 0
        not_aca_count = 0
        not_strict_count = 0

        for x in range(iter_count):
            data_generation = DataGeneration()
            history = History(data_generation.generate_transactions())
            history.interleave_transaction_schedule()
            recovery_engine = RecoveryEngine(history)
            report = recovery_engine.get_report()

            if report.is_not_recoverable():
                not_recoverable_count += 1
            
            if report.is_not_aca():
                not_aca_count += 1

            if report.is_not_strict():
                not_strict_count += 1

        results.append({
            'not_recoverable_percent': (not_recoverable_count/iter_count) * 100,
            'not_cacadeless_percent': (not_aca_count/iter_count) * 100,
            'not_strict_percent': (not_strict_count/iter_count) * 100,
        })
    
    AppConfig.restore_defaults()
    return results
    
def build_transaction_graph():
    iter_count = 100

    results = []
    
    for idx in range(10):
        AppConfig.set('transaction_count', { 'min': 1, 'max': idx+1 })

        not_recoverable_count = 0
        not_aca_count = 0
        not_strict_count = 0

        for x in range(iter_count):
            data_generation = DataGeneration()
            history = History(data_generation.generate_transactions())
            history.interleave_transaction_schedule()
            recovery_engine = RecoveryEngine(history)
            report = recovery_engine.get_report()

            if report.is_not_recoverable():
                not_recoverable_count += 1
            
            if report.is_not_aca():
                not_aca_count += 1

            if report.is_not_strict():
                not_strict_count += 1

        results.append({
            'not_recoverable_percent': (not_recoverable_count/iter_count) * 100,
            'not_cacadeless_percent': (not_aca_count/iter_count) * 100,
            'not_strict_percent': (not_strict_count/iter_count) * 100,
        })
    
    AppConfig.restore_defaults()
    return results

