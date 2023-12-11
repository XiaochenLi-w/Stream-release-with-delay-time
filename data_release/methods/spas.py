import math
#from pegasus_d import perturb_l
import numpy as np
import random
import matplotlib.pyplot as plt
# import pickle
# import copy

# num: number of random noisy value

UP_TS = 2.3
DIS_SAMPLE_W_NUM = 1

def add_noise(sensitivity, eps, num):
    noisy_arr = []
    if num > 1:
        for i in range(num):
            tmp = np.random.laplace(loc=0,scale=sensitivity/eps)
            noisy_arr.append(tmp)
                
        return noisy_arr
        
    else:
        return np.random.laplace(loc=0,scale=sensitivity/eps)


def count_varavgdis(op_arr, window_size):
    sum = 0
    num = len(op_arr)

    for i in range(DIS_SAMPLE_W_NUM * window_size - 1):
        sum += (op_arr[num - i - 1] - op_arr[num - i - 2]) ** 2


    return sum / (window_size - 1)
    


def count_optimalc(eps, sensitivity_, var_avgdis):
    optimal_c = int(eps * math.sqrt(3 * var_avgdis) / (6 * sensitivity_))
    optimal_c = max(1, optimal_c)

    # optimal_c = int(min((self.para_eps -self.para_eps * 1 / 4 /self.para_d) * self.avg_dis(self.old_pc_para, op_arr) / 2.3, self.para_w))

    return optimal_c

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


# no warm-up
def spas(ex, eps, sensitivity_, window_size):
    init_c = min(window_size, int(5 + eps / (window_size / 120) * 15))
    total_time = len(ex)
    dim = len(ex[0])
    eps_svt = eps / 4
    eps_pub = eps - eps_svt
    eps_1 = eps_svt / 2
    eps_2 = eps_svt / 2

    optimal_c = init_c
    published_result = []
    consum_eps = []
    rho_ = add_noise(sensitivity_, eps_1, 1)

    for i in range(total_time):
        if i < window_size:
            if i % int(window_size / optimal_c) == 0:
                noise_result = ex[i][0] + add_noise(sensitivity_, eps_pub / optimal_c, dim)
                published_result.append(noise_result)
                consum_eps.append(eps_pub / optimal_c)
            else:
                published_result.append(published_result[i - 1])
                consum_eps.append(0)

        else:
            if (ex[i][0] - published_result[i - 1]) + add_noise(sensitivity_, eps_2 / (2 * optimal_c), 1) > sensitivity_ * optimal_c / eps_pub + rho_ and budget_enough(i, eps_pub / optimal_c, consum_eps, eps_pub, window_size):
                noise_result = ex[i][0] + add_noise(sensitivity_, eps_pub / optimal_c, dim)
                published_result.append(noise_result)
                consum_eps.append(eps_pub / optimal_c)

                var_avgdis = count_varavgdis(published_result, window_size)
                optimal_c = count_optimalc(eps_pub, sensitivity_, var_avgdis)
                #print(optimal_c)
            else:
                published_result.append(published_result[i - 1])
                consum_eps.append(0)


    return published_result

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

def run_spas(ex, epsilon_list, sensitivity_, window_size, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = spas(ex, eps, sensitivity_, window_size)
            err_round += count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_

if __name__ == "__main__":

    count = 0
    ex = []
    filename = "./data/unemployment.csv"
    with open(filename, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')        
                ex.append([int(tmp[-1])])

    # filename = "./data/ILINet.csv"
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

    round_ = 10
    window_size = 100
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    sensitivity_ = max(data) - min(data)

    error_ = run_spas(ex, epsilon_list, sensitivity_, window_size, round_)
    print(error_)
    
    plt.plot(epsilon_list, error_)
    plt.show()