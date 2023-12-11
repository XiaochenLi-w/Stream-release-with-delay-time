import numpy as np
import random
import math
import delay_spas
import matplotlib.pyplot as plt

def count_mae(ex, published_result):
    total_time = len(ex)
    published_time = len(published_result)
    #print(total_time, published_time)

    if total_time != published_time:
        print("error")
        return
    
    error_sum = 0

    for i in range(published_time):
        error_sum += abs(ex[i][0] - published_result[i])
    
    return error_sum / published_time

def naive_event(ex, sensitivity_, eps):
    total_time = len(ex)
    dim = len(ex[0])

    published_result = []

    for i in range(total_time):
        noise_result = ex[i][0] + delay_spas.add_noise(sensitivity_, eps, dim)
        published_result.append(noise_result)
    
    return published_result

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


# def ordered_noise(buc_num, buc_size, eps, sensitivity_):
#     num_in_buc = 100
#     noise_pool = np.zeros((buc_num, num_in_buc), dtype=float)
#     noises = np.zeros(buc_num * num_in_buc, dtype= float)

#     for i in range(buc_num * num_in_buc):
#         noises[i] = delay_spas.add_noise(sensitivity_, eps, 1)
    
#     noises = np.sort(noises)
#     c = 0

#     for i in range(buc_num):
#         for j in range(num_in_buc):
#             noise_pool[i][j] = noises[c]
#             c += 1

#     return noise_pool

# def order_advance(ex, sensitivity_, eps, delay_time, buc_size):
#     total_time = len(ex)
#     eps_buc = eps / 4
#     eps_pub = eps - eps_buc
    
#     buc_num = int(np.ceil(delay_time / buc_size))
    
#     published_result = []

#     for i in range(total_time // delay_time):
#         noise_pool = ordered_noise(buc_num, buc_size, eps_pub, sensitivity_)
#         data_batch = np.zeros(delay_time, dtype=int)
#         c = 0
#         for j in range(i * delay_time, (i + 1) * delay_time):
#             data_batch[c] = ex[j][0]
#             c += 1

#         order_index = np.argsort(data_batch)
#         buc_alloc = np.zeros(delay_time, dtype=int)
#         for j in range(delay_time):
#             idex_ = order_index[j]
#             buc_alloc[idex_] = j // buc_size

#         noise_bucalloc = randomized_response(buc_alloc, buc_num, eps_buc)
#         num_in_buc = 100
        
#         for j in range(delay_time):
#             release_value = data_batch[j] + noise_pool[noise_bucalloc[j]][np.random.randint(0, num_in_buc)]
#             published_result.append(release_value)

#     if total_time % delay_time > 0:
#         remain_num = total_time % delay_time
#         buc_num = int(np.ceil(remain_num / buc_size))
#         noise_pool = ordered_noise(buc_num, buc_size, eps_pub, sensitivity_)
#         data_batch = np.zeros(remain_num, dtype=int)
#         c = 0
#         for j in range((total_time // delay_time) * delay_time, total_time):
#             data_batch[c] = ex[j][0]
#             c += 1

#         order_index = np.argsort(data_batch)
#         buc_alloc = np.zeros(remain_num, dtype=int)
#         for j in range(remain_num):
#             idex_ = order_index[j]
#             buc_alloc[idex_] = j // buc_size

#         noise_bucalloc = randomized_response(buc_alloc, buc_num, eps_buc)
        
#         for j in range(remain_num):
#             release_value = data_batch[j] + noise_pool[noise_bucalloc[j]][np.random.randint(0, num_in_buc)]
#             published_result.append(release_value)
    
#     return published_result

def order_advance(ex, sensitivity_, eps, delay_time, buc_size):
    total_time = len(ex)
    eps_buc = eps / 4
    eps_pub = eps - eps_buc
    
    buc_num = int(np.ceil(delay_time / buc_size))
    
    published_result = []

    for i in range(total_time // delay_time):
        data_batch = np.zeros(delay_time, dtype=int)
        c = 0
        for j in range(i * delay_time, (i + 1) * delay_time):
            data_batch[c] = ex[j][0]
            c += 1

        order_index = np.argsort(data_batch)
        buc_alloc = np.zeros(delay_time, dtype=int)
        for j in range(delay_time):
            idex_ = order_index[j]
            buc_alloc[idex_] = j // buc_size

        noise_bucalloc = randomized_response(buc_alloc, buc_num, eps_buc)
        buc_sum = np.zeros(buc_num, dtype=float)
        
        for j in range(delay_time):
            buc_sum[noise_bucalloc[j]] += data_batch[j]

        for j in range(buc_num):
            buc_sum[j] += delay_spas.add_noise(sensitivity_, eps_pub, 1)
            if j > 0 and buc_sum[j] < buc_sum[j - 1]:
                #buc_sum[j] = buc_sum[j - 1] + buc_size * (buc_size - 1) / 2
                buc_sum[j] = buc_sum[j - 1]

        for j in range(delay_time):
            release_value = buc_sum[noise_bucalloc[j]] / buc_size
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
        
        for j in range(remain_num):
            buc_sum[noise_bucalloc[j]] += data_batch[j]

        for j in range(buc_num):
            buc_sum[j] += delay_spas.add_noise(sensitivity_, eps_pub, 1)
            if j > 0 and buc_sum[j] < buc_sum[j - 1]:
                buc_sum[j] = buc_sum[j - 1] + buc_size * (buc_size - 1) / 2

        for j in range(remain_num):
            release_value = buc_sum[noise_bucalloc[j]] / buc_size
            published_result.append(release_value)
    
    return published_result

def run_naive_event(ex, sensitivity_, epsilon_list, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = naive_event(ex, sensitivity_, eps)
            err_round += count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_

def run_order_advance(ex, sensitivity_, epsilon_list, round_, delay_time, buc_size):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = order_advance(ex, sensitivity_, eps, delay_time, buc_size)
            err_round += count_mae(ex, published_result)

        error_.append(err_round / round_)

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
    sensitivity_ = max(data) - min(data)
    
    buc_size = 10

    error_1 = run_naive_event(ex, sensitivity_, epsilon_list, round_)
    error_2 = run_order_advance(ex, sensitivity_, epsilon_list, round_, delay_time, buc_size)
    print(error_1)
    print(error_2)
    
    plt.plot(epsilon_list, error_1, label='naive')
    plt.plot(epsilon_list, error_2, label='order_adv')
    plt.legend()
    plt.show()