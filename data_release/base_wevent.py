import math
import numpy as np
import random
import matplotlib.pyplot as plt

def count_mae(ex, published_result):
    total_time = len(ex)
    published_time = len(published_result)

    if total_time != published_time:
        print("error")
        return
    
    error_sum = 0

    for i in range(published_time):
        error_sum += abs(ex[i][0] - published_result[i])
    
    return error_sum / published_time

def add_noise(sensitivity, eps, num):
    noisy_arr = []
    if num > 1:
        for i in range(num):
            tmp = np.random.laplace(loc=0,scale=sensitivity/eps)
            noisy_arr.append(tmp)
                
        return noisy_arr
        
    else:
        return np.random.laplace(loc=0,scale=sensitivity/eps)

def uniform_wevent(ex, eps, sensitivity_, window_size):
    total_time = len(ex)

    published_result = []

    for i in range(total_time):
        published_result.append(ex[i][0] + add_noise(sensitivity_, eps / window_size, 1))

    return published_result

def sample_wevent(ex, eps, sensitivity_, window_size):
    total_time = len(ex)

    published_result = []

    for i in range(total_time):
        if i % window_size == 0:
            published_result.append(ex[i][0] + add_noise(sensitivity_, eps, 1))
        else:
            published_result.append(published_result[i - 1])

    return published_result

def run_uniform(ex, epsilon_list, sensitivity_, window_size, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = uniform_wevent(ex, eps, sensitivity_, window_size)
            err_round += count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_

def run_sample(ex, epsilon_list, sensitivity_, window_size, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = sample_wevent(ex, eps, sensitivity_, window_size)
            err_round += count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_

if __name__ == "__main__":

    count = 0
    ex = []
    filename = "./data/unemployment.csv"
    # with open(filename, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 3:
    #             tmp = lines.split(',')        
    #             ex.append([int(tmp[-1])])

    filename = "./data/ILINet.csv"
    with open(filename, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')
                
                ex.append([int(tmp[-3])])
    
    data = np.zeros(len(ex), dtype=int)
    for i in range(len(ex)):
        data[i] = ex[i][0]

    round_ = 10
    window_size = 100
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    sensitivity_ = max(data) - min(data)

    error_1 = run_uniform(ex, epsilon_list, sensitivity_, window_size, round_)
    error_2 = run_sample(ex, epsilon_list, sensitivity_, window_size, round_)
    print(error_1)
    print(error_2)
    
    plt.plot(epsilon_list, error_1, label='uniform')
    plt.plot(epsilon_list, error_2, label='sample')
    plt.legend()
    plt.show()