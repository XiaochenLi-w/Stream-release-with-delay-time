import numpy as np
import matplotlib.pyplot as plt

import methods.common_tools
import methods.naive
import methods.sensitivity_calc

def comporder(ex, domain_low, domain_high, eps, delay_time, flag = 0, interval_ = 5, num_ = 100):
    total_time = len(ex)
    dim = len(ex[0])
    eps_post = eps / 4
    eps_pub = eps - eps_post
    eps_1 = eps_post / 2
    eps_2 = eps_post / 2

    published_result = []
    flag_ = []

    whether_update = 0
    sensitivity_ = domain_high

    rho_ = methods.common_tools.add_noise(sensitivity_, eps_1 / 2, dim)

    for i in range(total_time):
        if whether_update == 0:
            eps_pub = eps - eps_post
        
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

        temp = []
        if i + delay_time < total_time:
            for j in range(i + 1, i + delay_time):
                if ex[i][0] - ex[j][0] + methods.common_tools.add_noise(sensitivity_, eps_2 / (2 * (2 * delay_time - 1)), dim) > rho_:
                #if ex[i][0] - ex[j][0] > 0:
                    temp.append(0)
                else:
                    temp.append(1)
        elif i + 1 < total_time:
            for j in range(i + 1, total_time):
                if ex[i][0] - ex[j][0] + methods.common_tools.add_noise(sensitivity_, eps_2 / (2 * (2 * delay_time - 1)), dim) > rho_:
                #if ex[i][0] - ex[j][0] > 0:
                    temp.append(0)
                else:
                    temp.append(1)
        else:
            temp = []
        
        flag_.append(temp)
        
        low_ = 0
        high_ = 1000000000
        if i > delay_time - 1:
            for j in range(i - delay_time + 1, i - 1):
                if flag_[j][i - j - 1] == 0:
                    if published_result[j] > low_:
                        low_ = published_result[j]
                else:
                    if published_result[j] < high_:
                        high_ = published_result[j]
        else:
            for j in range(0, i - 1):
                if flag_[j][i - j - 1] == 0:
                    if published_result[j] > low_:
                        low_ = published_result[j]
                else:
                    if published_result[j] < high_:
                        high_ = published_result[j]
        
        if noise_result > low_ or noise_result < high_:
            if low_ > high_:
                noise_result = (low_ + high_) / 2

        published_result.append(noise_result)

    return published_result


def run_comporder(ex, domain_low, domain_high, epsilon_list, round_, delay_time, flag = 0, interval_ = 5, num_ = 100):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = comporder(ex, domain_low, domain_high, eps, delay_time, flag, interval_, num_)
            err_round += methods.common_tools.count_mae(ex, published_result)
            #print('round', j, 'over!')

        error_.append(err_round / round_)
    
    print('Order_based:', error_)

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
    
    data = np.zeros(len(ex), dtype=int)
    for i in range(len(ex)):
        data[i] = ex[i][0]

    round_ = 10
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    delay_time = 100
    sensitivity_ = max(data)

    error_1 = methods.naive.run_naive_event(ex, max(data), epsilon_list, round_)
    error_2 = run_comporder(ex, min(data), max(data), epsilon_list, round_, delay_time, 1)
    print(error_1)
    print(error_2)
    
    plt.plot(epsilon_list, error_1, label='naive')
    plt.plot(epsilon_list, error_2, label='comporder')
    plt.legend()
    plt.show()