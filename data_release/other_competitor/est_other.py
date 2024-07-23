import os
import sys
ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT)

import numpy as np
import matplotlib.pyplot as plt

from other_competitor.adapub import Adapub

def count_mae(ex, published_result):
    total_time = len(ex)
    published_time = len(published_result)
    #print(total_time, published_time)

    if total_time != published_time:
        print("error")
        return
    
    error_sum = 0

    for i in range(published_time):
        error_sum += abs(ex[i][0] - published_result[i][0])
    
    return error_sum / published_time

def est_sens_opt(ex_, domain_low, domain_high, epsilon_list, round_):
    
    error_adapub = []
    for para_eps in epsilon_list:
        error_ = 0
        mech = Adapub(para_eps, len(ex_), 1)
    
        for r in range(round_):
            op, publish_num = mech.run(ex_, domain_high)
            error_ += count_mae(ex_, op)
        
        error_adapub.append(error_/round_)
    

    print(error_adapub)


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
        epsilon_list = [0.1, 0.5, 1.0]
        print('data domain:', min(data), max(data))

        est_sens_opt(ex[k], min(data), max(data), epsilon_list, round_)
    