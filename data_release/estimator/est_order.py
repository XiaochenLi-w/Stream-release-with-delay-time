import os
import sys
ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT)

import numpy as np
import matplotlib.pyplot as plt

import methods.compOrder
import methods.bucOrder
import methods.common_tools

def est_bucorder(ex, domain_low, domain_high, epsilon_list, round_, tau, buc_list, delay_time, flag = 0, interval_ = 5, num_ = 100):

    error_draw = np.zeros([len(epsilon_list), len(buc_list)], dtype=float)
    error = []

    for buc_size in buc_list:
        error_order = methods.bucOrder.run_order_advance(ex, domain_low, domain_high, epsilon_list, round_, delay_time, buc_size, flag, interval_)
        error.append(error_order)

    print(error)

    plt.plot(buc_list, error)
    plt.legend()
    plt.show()

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
        #epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        epsilon_list = [0.4, 0.6, 1.0]
        delay_time = 100
        #delay_time_list = [10, 30, 50, 70, 90]
        tau = 3
        if filename[k] == './data_release/data/ILINet.csv':
            buc_list = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
        else:
            buc_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        #buc_list = [100]
        print('data domain:', min(data), max(data))
        #sensitivity_ = 1

        est_bucorder(ex[k], min(data), max(data), epsilon_list, round_, tau, buc_list, delay_time, 0)
        #est_bucorder_delay(ex[k], min(data), max(data), epsilon_list, round_, tau, buc_size, delay_time_list, 0)
    