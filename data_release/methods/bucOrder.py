import numpy as np
import random
import math
import matplotlib.pyplot as plt

import methods.common_tools
import methods.naive
import methods.sensitivity_calc

def randomized_response(data, k, eps):
    p = math.exp(eps) / (math.exp(eps) + k - 1)
    noise_results = np.zeros(len(data), dtype=int)
    for idx, num in enumerate(data):
        randomized_value = num 
        if random.random() > p:
            while randomized_value == num: 
                randomized_value = np.random.randint(0, k)
        noise_results[idx] = randomized_value

    return noise_results


def order_advance(ex, domain_low, domain_high, eps, delay_time, buc_size, flag = 0, interval_ = 5):
    total_time = len(ex)
    eps_buc = eps / 4
    eps_pub = eps - eps_buc
    
    buc_num = int(np.ceil(domain_high / buc_size))
    
    published_result = []

    sensitivity_ = domain_high

    for i in range(total_time // delay_time):
        eps_pub = eps - eps_buc
        data_batch = np.zeros(delay_time, dtype=int)
        c = 0
        if flag == 1 and i % interval_ == 0 and (i + 1) * delay_time<= total_time:
            eps_s = eps_pub / 2
            eps_pub = eps_pub - eps_s

            data_sens = np.zeros(delay_time, dtype = int)
            cc = 0
            for qq in range(i * delay_time, (i + 1) * delay_time):
                data_sens[cc] = ex[qq][0]
                cc += 1

            sensitivity_ = methods.sensitivity_calc.quality_func(data_sens, domain_low, domain_high, interval_, eps_s)

        for j in range(i * delay_time, (i + 1) * delay_time):
            data_batch[c] = ex[j][0]
            if ex[j][0] > sensitivity_:
                data_batch[c] = sensitivity_
            c += 1

        buc_alloc = np.zeros(delay_time, dtype=int)
        for j in range(delay_time):
            buc_alloc[j] = data_batch[j] // buc_size

        noise_bucalloc = randomized_response(buc_alloc, buc_num, eps_buc)
        buc_sum = np.zeros(buc_num, dtype=float)
        buc_innernum = np.zeros(buc_num, dtype=int)
        
        for j in range(delay_time):
            buc_innernum[noise_bucalloc[j]] += 1
            buc_sum[noise_bucalloc[j]] += data_batch[j]

        for j in range(buc_num):
            buc_sum[j] += methods.common_tools.add_noise(sensitivity_, eps_pub, 1)
            if j > 0 and buc_sum[j] < buc_sum[j - 1]:
                #buc_sum[j] = buc_sum[j - 1] + buc_size * (buc_size - 1) / 2
                buc_sum[j] = buc_sum[j - 1]
            if buc_sum[j] < j * buc_size * buc_innernum[j]:
                buc_sum[j] = j * buc_size * buc_innernum[j]
            if buc_sum[j] > (j + 1) * buc_size * buc_innernum[j] - 1:
                buc_sum[j] = (j + 1) * buc_size * buc_innernum[j] - 1

        for j in range(delay_time):
            release_value = buc_sum[noise_bucalloc[j]] / buc_innernum[noise_bucalloc[j]]
            published_result.append(release_value)

    if total_time % delay_time > 0:
        remain_num = total_time % delay_time
        buc_num = int(np.ceil(remain_num / buc_size))
        data_batch = np.zeros(remain_num, dtype=int)
        c = 0
        for j in range((total_time // delay_time) * delay_time, total_time):
            data_batch[c] = ex[j][0]
            c += 1

        order_index = np.argsort(data_batch)
        buc_alloc = np.zeros(remain_num, dtype=int)
        for j in range(remain_num):
            idex_ = order_index[j]
            buc_alloc[idex_] = j // buc_size

        noise_bucalloc = randomized_response(buc_alloc, buc_num, eps_buc)
        buc_sum = np.zeros(buc_num, dtype=float)
        buc_innernum = np.zeros(buc_num, dtype=int)
        
        for j in range(remain_num):
            buc_innernum[noise_bucalloc[j]] += 1
            buc_sum[noise_bucalloc[j]] += data_batch[j]

        for j in range(buc_num):
            buc_sum[j] += methods.common_tools.add_noise(sensitivity_, eps_pub, 1)
            if j > 0 and buc_sum[j] < buc_sum[j - 1]:
                buc_sum[j] = buc_sum[j - 1] + buc_size * (buc_size - 1) / 2
            if buc_sum[j] < j * buc_size * buc_innernum[j]:
                buc_sum[j] = j * buc_size * buc_innernum[j]
            if buc_sum[j] > (j + 1) * buc_size * buc_innernum[j] - 1:
                buc_sum[j] = (j + 1) * buc_size * buc_innernum[j] - 1

        for j in range(remain_num):
            release_value = buc_sum[noise_bucalloc[j]] / buc_innernum[noise_bucalloc[j]]
            published_result.append(release_value)
    
    return published_result


def run_order_advance(ex, domain_low, domain_high, epsilon_list, round_, delay_time, buc_size, flag = 0, interval_ = 5):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = order_advance(ex, domain_low, domain_high, eps, delay_time, buc_size, flag, interval_)
            err_round += methods.common_tools.count_mae(ex, published_result)

        error_.append(err_round / round_)

    print('BucOrder:', error_)

    return error_

if __name__ == "__main__":

    count = 0
    ex = []
    filename = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/unemployment.csv"
    with open(filename, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')        
                ex.append([int(tmp[-1])])
    
    # filename = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/ILINet.csv"
    # with open(filename, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 3:
    #             tmp = lines.split(',')
                
    #             ex.append([int(tmp[-3])])

    data = np.zeros(len(ex), dtype=int)
    for i in range(len(ex)):
        data[i] = ex[i][0]

    round_ = 1
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    delay_time = 100
    
    buc_size = 100

    error_1 = methods.naive.run_naive_event(ex, max(data), epsilon_list, round_)
    error_2 = run_order_advance(ex, min(data), max(data), epsilon_list, round_, delay_time, buc_size, 0)
    print(error_1)
    print(error_2)
    
    #plt.plot(epsilon_list, error_1, label='naive')
    plt.plot(epsilon_list, error_2, label='order_adv')
    plt.legend()
    plt.show()