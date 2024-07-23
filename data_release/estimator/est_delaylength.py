import os
import sys
ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT)

import numpy as np
import matplotlib.pyplot as plt

import methods.compOrder
import methods.bucOrder
import methods.discontinuous
# import methods.common_tools

def est_bucorder_delay(ex, domain_low, domain_high, epsilon_list, round_, tau, buc_size, delay_time_list, flag = 0, interval_ = 5, num_ = 100):

    error_buc = []

    for delay_time in delay_time_list:
        error_order = methods.bucOrder.run_order_advance(ex, domain_low, domain_high, epsilon_list, round_, delay_time, buc_size, flag, interval_)
        error_buc.append(error_order[0])

    error_comp = []

    for delay_time in delay_time_list:
        error_order = methods.compOrder.run_comporder(ex, domain_low, domain_high, epsilon_list, round_, delay_time, flag, interval_, num_)
        error_comp.append(error_order[0])

    error_contin = []

    for delay_time in delay_time_list:
        error_order = methods.discontinuous.run_discontin_reduce(ex, domain_low, domain_high, epsilon_list, round_, delay_time, tau, flag, interval_)
        error_contin.append(error_order[0])
    
    print('*************Results*****************')
    print('Discontinuous:', error_contin)
    print('CompOrder:', error_comp)
    print('BucOrder:', error_buc)
    print('*************Results End******************')


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
        epsilon_list = [0.5]
        delay_time = 100
        delay_time_list = [10, 30, 50, 70, 90]
        tau = 3
        if filename[k] == './data_release/data/ILINet.csv':
            buc_size = 10000
        else:
            buc_size = 100

        print('data domain:', min(data), max(data))

        est_bucorder_delay(ex[k], min(data), max(data), epsilon_list, round_, tau, buc_size, delay_time_list, 0)
    