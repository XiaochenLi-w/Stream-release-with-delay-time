import numpy as np
import matplotlib.pyplot as plt

import methods.common_tools
import methods.sensitivity_calc

def naive_event(ex, sensitivity_, eps):
    total_time = len(ex)
    dim = len(ex[0])

    published_result = []

    for i in range(total_time):
        noise_result = ex[i][0] + methods.common_tools.add_noise(sensitivity_, eps, dim)
        published_result.append(noise_result)

    return published_result


def naive_sens(ex, domain_low, domain_high, eps, flag = 0, interval_ = 5, num_ = 100):
    total_time = len(ex)
    dim = len(ex[0])

    published_result = []
    eps_pub = eps

    whether_update = 0
    sensitivity_ = domain_high

    for i in range(total_time):
        if whether_update == 0:
            eps_pub = eps
        
        if i % num_ == 0:
            if (i / num_) % interval_ == 0 and flag == 1 and (i + 1) * num_ <= total_time:
                eps_s = eps_pub / 2
                eps_pub = eps_pub - eps_s

                data_sens = np.zeros(num_, dtype = int)
                cc = 0
                for qq in range(i * num_, (i + 1) * num_):
                    data_sens[cc] = ex[qq][0]
                    cc += 1

                sensitivity_ = methods.sensitivity_calc.quality_func(data_sens, domain_low, domain_high, interval_, eps_s)
                whether_update = 1
            else:
                whether_update = 0

        if ex[i][0] > sensitivity_:
            noise_result = sensitivity_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
        else:
            noise_result = ex[i][0] + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
   
        published_result.append(noise_result)

    return published_result


def run_naive_event(ex, sensitivity_, epsilon_list, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = naive_event(ex, sensitivity_, eps)
            err_round += methods.common_tools.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('naive:', error_)

    return error_


def run_naive_sens(ex, domain_low, domain_high, epsilon_list, round_, flag = 0, interval_ = 5, num_ = 100):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = naive_sens(ex, domain_low, domain_high, eps, flag, num_)
            err_round += methods.common_tools.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('naive:', error_)

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

    round_ = 1
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]

    error_1 = run_naive_event(ex, max(data), epsilon_list, round_)
    error_2 = run_naive_sens(ex, min(data), max(data), epsilon_list, round_, 1, 5, 100)
    print(error_1)
    print(error_2)
    
    plt.plot(epsilon_list, error_1, label='naive')
    plt.plot(epsilon_list, error_2, label='naive_sens')
    plt.legend()
    plt.show()