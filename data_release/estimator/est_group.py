import os
import sys
ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT)

import numpy as np
import matplotlib.pyplot as plt

import methods.continuous
import methods.discontinuous
# import methods.common_tools

def est_group(ex, domain_low, domain_high, epsilon_list, round_, tau_list, delay_time, flag = 0, interval_ = 5, num_ = 100):
    
    print('Continuous group-based approach, noise is added to the summation.')
    for tau in tau_list:
        print('tau:', tau)
        methods.continuous.run_reduce_noise_continuous(ex, domain_low, domain_high, epsilon_list, round_, tau, delay_time, flag, interval_)
    
    print('Continuous group-based approach, noise is added to the individual data.')
    for tau in tau_list:
        print('tau:', tau)
        methods.continuous.run_pegasus_delay(ex, domain_low, domain_high, epsilon_list, round_, tau, flag, interval_, num_)

    print('Discontinuous group-based approach, noise is added to the summation.')
    for tau in tau_list:
        print('tau:', tau)
        methods.discontinuous.run_discontin_reduce(ex, domain_low, domain_high, epsilon_list, round_, delay_time, tau, flag, interval_)
    
    print('Discontinuous group-based approach, noise is added to the individual data.')
    for tau in tau_list:
        print('tau:', tau)
        methods.discontinuous.run_discontin_post(ex, domain_low, domain_high, epsilon_list, round_, delay_time, tau, flag, interval_)


if __name__ == "__main__":

    ex = []
    filename = []
    
    count = 0
    ex2 = []
    filename2 = "./data_release/data/unemployment.csv"
    with open(filename2, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')        
                ex2.append([int(tmp[-1])])

    ex.append(ex2)
    filename.append(filename2)

    count = 0
    ex3 = []
    filename3 = "./data_release/data/ILINet.csv"
    with open(filename3, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')        
                ex3.append([int(float(tmp[-1]))])

    ex.append(ex3)
    filename.append(filename3)

    for k in range(len(ex)):
        print('#It is the results of', filename[k])

        length_ = len(ex[k])
        data = np.zeros(length_, dtype=int)
        for i in range(length_):
            data[i] = ex[k][i][0]

        round_ = 20
        epsilon_list = [0.4]
        delay_time = 100
        tau_list = [1, 5, 9, 13, 17]
        print('data domain:', min(data), max(data))

        est_group(ex[k], min(data), max(data), epsilon_list, round_, tau_list, delay_time, 0)
    