import os
import sys
ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT)

import numpy as np
import matplotlib.pyplot as plt

import methods.naive
import methods.continuous
import methods.discontinuous
import methods.compOrder
import methods.bucOrder
import methods.common_tools

def est_sens_opt(ex, domain_low, domain_high, epsilon_list, round_, tau, buc_size, delay_time, flag = 0, interval_ = 5, num_ = 100):
    
    error_naive = methods.naive.run_naive_sens(ex, domain_low, domain_high, epsilon_list, round_, flag, interval_, num_)
    
    # group-based methods
    error_pegasus_delay = methods.continuous.run_pegasus_delay(ex, domain_low, domain_high, epsilon_list, round_, tau, flag, interval_, num_)
    error_discontinpp = methods.discontinuous.run_discontin_post(ex, domain_low, domain_high, epsilon_list, round_, delay_time, tau, flag, interval_)
    
    # order-based methods
    error_order = methods.compOrder.run_comporder(ex, domain_low, domain_high, epsilon_list, round_, delay_time, flag, interval_, num_)
    error_order_advance = methods.bucOrder.run_order_advance(ex, domain_low, domain_high, epsilon_list, round_, delay_time, buc_size, flag, interval_)
     

    # print('Naive:', error_naive)
    # print('Contin:', error_pegasus_delay)
    # print('Discontin:', error_discontinpp)
    # print('CompOrder:', error_order)
    # print('BucOrder:', error_order_advance)

if __name__ == "__main__":

    ex = []
    filename = []
    
    count = 0
    ex1 = []
    filename1 = "./data_release/data/COVID19_DEATH.csv"
    with open(filename1, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')
                
                ex1.append([int(float(tmp[-1]))])
    ex.append(ex1)
    filename.append(filename1)

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

    count = 0
    ex4 = []
    filename4 = "./data_release/data/footmart.csv"
    with open(filename4, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            else:
                tmp = lines.split(',')        
                ex4.append([int(float(tmp[-1]))])

    ex.append(ex4)
    filename.append(filename4)

    for k in range(len(ex)):
        print('#It is the results of', filename[k])

        length_ = len(ex[k])
        data = np.zeros(length_, dtype=int)
        for i in range(length_):
            data[i] = ex[k][i][0]

        round_ = 20
        epsilon_list = [0.5]
        delay_time = 100
        tau = 3
        buc_size = 100
        # this dataset's domain size is too large
        if filename[k] == './data_release/data/ILINet.csv':
            buc_size = 10000
        print('data domain:', min(data), max(data))
        
        # real data stream: ex[k], data domain: [min(data), max(data)], epsilon: epsilon_list, run times: round_, 
        # similarity threshold(group-based method): tau_, size of bucket(BucOrder): buc_size, 
        # number of timestamps for delay: delay_time, Whether reduce sensitivity: Flag_=0(No), Flag=1(Yes)
        print('*****No Sensitivity Reduce*****')
        est_sens_opt(ex[k], min(data), max(data), epsilon_list, round_, tau, buc_size, delay_time, 0)
        print('*****Sensitivity Reduce*****')
        est_sens_opt(ex[k], min(data), max(data), epsilon_list, round_, tau, buc_size, delay_time, 1)