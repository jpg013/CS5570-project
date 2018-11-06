from history import History
from history_query_builder import HistoryQueryBuilder
from data_generation import DataGeneration
from recovery_engine import RecoveryEngine
from serializable_or_not import serializable_or_not
from app_config import AppConfig
import matplotlib.pyplot as plt

def checks(hist):
    recovery_engine = RecoveryEngine(hist)
    report = recovery_engine.get_report()
    report.display_pretty()

    if(serializable_or_not(hist)):
        print("The history is serializable", end = "\n")
    else:
        print("The history is not serializable", end = "\n")

def main():
    #not_recoverable_hist_input = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] c2 w1[z] c1'
    #not_recoverable_hist = HistoryQueryBuilder(not_recoverable_hist_input).process()
    
    #checks(not_recoverable_hist)
    """
    recoverable_not_aca_input = 'w1[x] w1[y] r2[u] w2[x] r2[y] w2[y] w1[z] c1 c2'
    recoverable_not_aca_hist = HistoryQueryBuilder(recoverable_not_aca_input).process()

    checks(recoverable_not_aca_hist)
 
    aca_not_strict_input = 'w1[x] w1[y] r2[u] w2[x] w1[z] c1 r2[y] w2[y] c2'
    aca_not_strict_hist = HistoryQueryBuilder(aca_not_strict_input).process()

    checks(aca_not_strict_hist)

    strict_input = 'r1[x] w1[x] c1 r2[x] w2[x] c2'
    strict_hist = HistoryQueryBuilder(strict_input).process()

    checks(strict_hist)

    not_serializable_input = "w1[x] w2[x] w2[y] c2 w1[y] w3[x] w3[y] c3 c1"
    not_serializable_hist = HistoryQueryBuilder(not_serializable_input).process()
    not_serializable_hist.print_pretty()

    checks(not_serializable_hist)
    """
    
if __name__== "__main__":
    #main()
    data_sets = [
        set(['x']),
        set(['x', 'y']),
        set(['x', 'y', 'z']),
        set(['x', 'y', 'z', 'u']),
        set(['x', 'y', 'z', 'u', 'q']),
        set(['x', 'y', 'z', 'u', 'q', 'r']),
        set(['x', 'y', 'z', 'u', 'q', 'r', 'p']),
        set(['x', 'y', 'z', 'u', 'q', 'r', 'p', 'i']),
    ]

    total_num = 10

    results = {}    
    
    for i in range(len(data_sets)):
        AppConfig.set('data_set', data_sets[i])

        num_recoverable = 0
        num_aca = 0
        num_strict = 0

        for x in range(total_num):
            data_gen = DataGeneration()
            hist = History(data_gen.generate_transactions())
            hist.interleave_transaction_schedule()   
            recovery_engine = RecoveryEngine(hist)
            report = recovery_engine.get_report()

            if report.is_recoverable():
                num_recoverable += 1

            if report.is_aca():
                num_aca += 1

            if report.is_strict():
                num_strict += 1

            if report.is_aca() and not report.is_recoverable():
                print('fatal')
                hist.print_pretty()

        results[str(i+1)] = {
            "recoverable": num_recoverable / total_num,
            "aca": num_aca / total_num,
            "strict": num_strict / total_num
        }

    result_items = results.items()
    rc = []
    aca = []
    st = []

    for item in result_items:
        rc.append(item[1].get('recoverable')*100)
        aca.append(item[1].get('aca')*100)
        st.append(item[1].get('strict')*100)

    # Data for plotting
    """
    #print(x_keys)
    fig, ax = plt.subplots()
    ax.plot(results.keys(), rc)
    ax.plot(results.keys(), aca)
    ax.plot(results.keys(), st)
    plt.gca().legend(('RC','ACA', 'ST'))
    ax.set(xlabel='max transaction count', ylabel='average percent',
       title='')
    ax.grid()
    plt.show()

    
# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
plt.show()
    
    total_num = 10000
    num_recoverable = 0
    num_aca = 0
    num_strict = 0

    transaction
    
    for i in range(total_num):
        hist = History(generate_transactions())
        hist.interleave_transaction_schedule()   
        recovery_engine = RecoveryEngine(hist)
        report = recovery_engine.get_report()
        
        if report.is_recoverable():
            num_recoverable += 1

        if report.is_aca():
            num_aca += 1

        if report.is_strict():
            num_strict += 1

    print(num_recoverable)
    print(num_aca)
    print(num_strict)

    year = [0, '20%', '40%', '60%', '80%', '100%']
    pop_pakistan = [44.91, 58.09, 78.07, 107.7, 138.5, 170.6]
    pop_india = [449.48, 553.57, 696.783, 870.133, 1000.4, 1309.1]
    plt.plot(pop_pakistan, year, color='g')
    plt.plot(pop_india, year, color='orange')
    plt.xlabel('Countries')
    plt.ylabel('Percent')
    plt.title('Average Percent of RC, ACA, ST')
    plt.show()
    """

    
    