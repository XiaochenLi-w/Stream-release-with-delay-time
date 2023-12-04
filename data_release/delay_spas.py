import math
import numpy as np
import random
import matplotlib.pyplot as plt
# import pickle
# import copy
import find_optimal_tau


def add_noise(sensitivity, eps, num):
    noisy_arr = []
    if num > 1:
        for i in range(num):
            tmp = np.random.laplace(loc=0,scale=sensitivity/eps)
            noisy_arr.append(tmp)
                
        return noisy_arr
        
    else:
        #return [np.random.laplace(loc=0,scale=sensitivity/eps)]
        return np.random.laplace(loc=0,scale=sensitivity/eps)


def budget_enough(index, eps_need, consum_eps, eps_pub, w):
    eps_sum = 0
    if len(consum_eps) < (w - 1):
        for i in range(len(consum_eps)):
            eps_sum += consum_eps[i]

    else:
        for i in range(index - w + 1, index):
            eps_sum += consum_eps[i]

    if eps_need + eps_sum > eps_pub:
        return False
    else:
        return True

def find_data_domain(ex):

    data = np.zeros(len(ex), dtype=int)
    for i in range(len(ex)):
        data[i] = ex[i][0]

    return max(data)

def spas_delay(ex, eps, sensitivity_, window_size, delay_time):
    total_time = len(ex)
    dim = len(ex[0])

    eps_svt = eps / 4
    #eps_svt = 0
    eps_pub = eps - eps_svt
    eps_1 = eps_svt / 2
    eps_2 = eps_svt / 2
    # sensitivity_pub = search_end
    # sensitivity_svt = search_end

    published_result = []
    consum_eps = []

    rho_ = add_noise(sensitivity_, eps_1, dim)

    for i in range(total_time - delay_time + 1):
        known_data = np.zeros(window_size + 1, dtype=int)
        if delay_time == window_size:
            # transfer the data to find_optimal_tau function
            if i == 0:
                noise_value = add_noise(sensitivity_, eps, dim)
                published_result.append(ex[i][0] + noise_value)
                consum_eps.append(0)
                continue
            else:
                known_data[0] = ex[i-1][0]
            #max_dis = 0
            c = 1
            for j in range(i, i + delay_time):
                known_data[c] = ex[j][0]
                # dis = known_data[c] - known_data[c - 1]
                # if dis > max_dis:
                #     max_dis = dis
                c += 1

            # if i == 0:
            #     optimal_tau, publish_count = find_optimal_tau.find_init_tau(known_data, window_size + 1, eps_pub, sensitivity_pub)
            #     publish_count = max(1, publish_count)
            #     print('init', optimal_tau, publish_count)
            # else:
                #optimal_tau, publish_count = find_optimal_tau.update_tau(known_data, search_start, search_end, window_size, eps_pub, sensitivity_pub, optimal_tau)
            optimal_tau, publish_count = find_optimal_tau.find_init_tau(known_data, window_size + 1, eps_pub, sensitivity_)
            publish_count = max(1, publish_count)
            #print('update', optimal_tau, publish_count)
            
            #print(optimal_tau, publish_count)
            if ((known_data[1] - known_data[0] + add_noise(sensitivity_, eps_2 / (2 * publish_count), 1)) > (optimal_tau + rho_)) and budget_enough(i, eps_pub / publish_count, consum_eps, eps_pub, window_size):
            #if ((known_data[1] - known_data[0]) > optimal_tau) and budget_enough(i, eps_pub / publish_count, consum_eps, eps_pub, window_size):
                noise_value = add_noise(sensitivity_, eps_pub / publish_count, dim)
                published_result.append(ex[i][0] + noise_value)
                consum_eps.append(eps_pub / publish_count)
            elif i == 0:
                noise_value = add_noise(sensitivity_, eps_pub / publish_count, dim)
                published_result.append(ex[i][0] + noise_value)
                consum_eps.append(eps_pub / publish_count)
            else:
                published_result.append(published_result[i-1]) 
                consum_eps.append(0)

    return (published_result)

def count_mae(ex, published_result, delay_time):
    total_time = len(ex) - delay_time + 1
    published_time = len(published_result)

    if total_time != published_time:
        print("error")
        return
    
    error_sum = 0

    for i in range(published_time):
        error_sum += abs(ex[i][0] - published_result[i])
    
    return error_sum / published_time

def run(ex, epsilon_list, sensitivity_, window_size, delay_time, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = spas_delay(ex, eps, sensitivity_, window_size, delay_time)
            err_round += count_mae(ex, published_result, delay_time)

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
    window_size = 100
    delay_time = window_size
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    sensitivity_ = max(data) - min(data)
    
    #epsilon_list = [0.1]

    error_ = run(ex, epsilon_list, sensitivity_, window_size, delay_time, round_)
    print(error_)
    
    plt.plot(epsilon_list, error_)
    plt.show()