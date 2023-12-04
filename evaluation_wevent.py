import matplotlib.pyplot as plt
import numpy as np
import delay_spas
import spas
import base_wevent

def run_delayspas(ex, epsilon_list, sensitivity_, window_size, delay_time, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = delay_spas.spas_delay(ex, eps, sensitivity_, window_size, delay_time)
            err_round += delay_spas.count_mae(ex, published_result, delay_time)

        error_.append(err_round / round_)

    return error_

def run_spas(ex, epsilon_list, sensitivity_, window_size, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = spas.spas(ex, eps, sensitivity_, window_size)
            err_round += spas.count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_

def run_uniform(ex, epsilon_list, sensitivity_, window_size, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = base_wevent.uniform_wevent(ex, eps, sensitivity_, window_size)
            err_round += base_wevent.count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_

def run_sample(ex, epsilon_list, sensitivity_, window_size, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = base_wevent.sample_wevent(ex, eps, sensitivity_, window_size)
            err_round += base_wevent.count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_

if __name__ == "__main__":

    count = 0
    ex = []
    # filename = "./data/unemployment.csv"
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
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    window_size = 120
    delay_time = window_size
    sensitivity_ = max(data) - min(data)

    error_delayspas = run_delayspas(ex, epsilon_list, sensitivity_, window_size, delay_time, round_)
    error_spas = run_spas(ex, epsilon_list, sensitivity_, window_size, round_)
    error_uniform = run_uniform(ex, epsilon_list, sensitivity_, window_size, round_)
    error_sample = run_sample(ex, epsilon_list, sensitivity_, window_size, round_)
    
    plt.plot(epsilon_list, error_delayspas, label='delay_spas')
    plt.plot(epsilon_list, error_spas, label='spas')
    plt.plot(epsilon_list, error_uniform, label='uniform')
    plt.plot(epsilon_list, error_sample, label='sample')
    plt.legend()
    plt.show()