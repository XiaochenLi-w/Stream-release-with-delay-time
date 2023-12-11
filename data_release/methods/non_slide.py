#-----------group-based post-processing----------

import numpy as np
import methods.delay_spas
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
        noise_result = ex[i][0] + methods.delay_spas.add_noise(sensitivity_, eps, dim)
        published_result.append(noise_result)

    return published_result


#----------judge wether invlove the data into a group
def whether_group(groupi, old_avg, new_data, tau, eps_group, sensitivity_, delay_time):
    total_num = len(groupi)
    new_avg = (old_avg * total_num + new_data) / (total_num + 1)
    #print(total_num)

    dev = 0
    for i in range(total_num):
        dev += abs(groupi[i] - new_avg)

    dev += abs(new_data - new_avg)

    #print(dev / total_num)

    if (dev / total_num) + methods.delay_spas.add_noise(sensitivity_ / total_num, eps_group / (4 * (2 * delay_time - 1)), 1) > tau + methods.delay_spas.add_noise(sensitivity_ / total_num, eps_group / (2 * (2 * delay_time - 1)), 1):
        return 0, new_avg
    else:
        return 1, new_avg


#------------discontinuous grouping in batch with post-processing-------------
def delay_noslide_event(ex, sensitivity_, eps, delay_time, tau):
    total_time = len(ex)
    dim = len(ex[0])
    eps_pub =4 * eps / 5
    eps_group = eps - eps_pub
    published_result = []

    i = 0
    
    for i in range(total_time):
        if i % delay_time == 0:
            if i > 0:
                results_indelay = np.zeros(delay_time, dtype=float)
                for j in range(len(group_)):
                    sum_ = 0
                    for k in range(len(group_[j])):
                        sum_ += group_[j][k] + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)
                    sum_ = sum_ / len(group_[j])
                    for k in range(len(group_[j])):
                        index = group_index[j][k]
                        results_indelay[index % delay_time] = sum_
        
                for j in results_indelay:
                    published_result.append(j)

            group_ = []
            group_index = []
            avg_ = []
            tmp = []
            tmp.append(ex[i][0])
            group_.append(tmp)
            avg_.append(ex[i][0])
            tmp = []
            tmp.append(i)
            group_index.append(tmp)
        else:
            num_group = len(group_)
            flag_ = False
            for j in range(num_group):
                ifadd_, newavg = whether_group(group_[j], avg_[j], ex[i][0], tau, eps_group, sensitivity_, delay_time)
                if ifadd_ == 1:
                    group_[j].append(ex[i][0])
                    avg_[j] = newavg
                    group_index[j].append(i)
                    flag_ = True
                    break
            if flag_ == False:
                tmp = []
                tmp.append(ex[i][0])
                group_.append(tmp)
                avg_.append(ex[i][0])
                tmp = []
                tmp.append(i)
                group_index.append(tmp)

        if i == total_time - 1:
                if total_time % delay_time == 0:
                    results_indelay = np.zeros(delay_time, dtype=float)
                else:
                    results_indelay = np.zeros(total_time % delay_time, dtype=float)
                for j in range(len(group_)):
                    sum_ = 0
                    for k in range(len(group_[j])):
                        sum_ += group_[j][k] + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)
                    sum_ = sum_ / len(group_[j])
                    for k in range(len(group_[j])):
                        index = group_index[j][k]
                        results_indelay[index % delay_time] = sum_
        
                for j in results_indelay:
                    published_result.append(j)

    #print(published_result)
    return published_result


#------------discontinuous grouping in batch with reduce noise-------------
def discontin_reduce(ex, sensitivity_, eps, delay_time, tau):
    total_time = len(ex)
    dim = len(ex[0])
    eps_pub =4 * eps / 5
    eps_group = eps - eps_pub
    published_result = []

    i = 0
    
    for i in range(total_time):
        if i % delay_time == 0:
            if i > 0:
                results_indelay = np.zeros(delay_time, dtype=float)
                for j in range(len(group_)):
                    sum_ = 0
                    for k in range(len(group_[j])):
                        sum_ += group_[j][k]
                    sum_ = (sum_ + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_[j])
                    for k in range(len(group_[j])):
                        index = group_index[j][k]
                        results_indelay[index % delay_time] = sum_
        
                for j in results_indelay:
                    published_result.append(j)

            group_ = []
            group_index = []
            avg_ = []
            tmp = []
            tmp.append(ex[i][0])
            group_.append(tmp)
            avg_.append(ex[i][0])
            tmp = []
            tmp.append(i)
            group_index.append(tmp)
        else:
            num_group = len(group_)
            flag_ = False
            for j in range(num_group):
                ifadd_, newavg = whether_group(group_[j], avg_[j], ex[i][0], tau, eps_group, sensitivity_, delay_time)
                if ifadd_ == 1:
                    group_[j].append(ex[i][0])
                    avg_[j] = newavg
                    group_index[j].append(i)
                    flag_ = True
                    break
            if flag_ == False:
                tmp = []
                tmp.append(ex[i][0])
                group_.append(tmp)
                avg_.append(ex[i][0])
                tmp = []
                tmp.append(i)
                group_index.append(tmp)

        if i == total_time - 1:
                if total_time % delay_time == 0:
                    results_indelay = np.zeros(delay_time, dtype=float)
                else:
                    results_indelay = np.zeros(total_time % delay_time, dtype=float)
                for j in range(len(group_)):
                    sum_ = 0
                    for k in range(len(group_[j])):
                        sum_ += group_[j][k]
                    sum_ = (sum_ + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_[j])
                    for k in range(len(group_[j])):
                        index = group_index[j][k]
                        results_indelay[index % delay_time] = sum_
        
                for j in results_indelay:
                    published_result.append(j)

    #print(published_result)
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


def run_delay_svt_event(ex, sensitivity_, epsilon_list, round_, delay_time, tau):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = delay_noslide_event(ex, sensitivity_, eps, delay_time, tau)
            err_round += count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_

def run_discontin_reduce(ex, sensitivity_, epsilon_list, round_, delay_time, tau):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = discontin_reduce(ex, sensitivity_, eps, delay_time, tau)
            err_round += count_mae(ex, published_result)

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

    round_ = 1
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    delay_time = 100
    tau = 3
    sensitivity_ = max(data) - min(data)

    error_1 = run_naive_event(ex, sensitivity_, epsilon_list, round_)
    error_2 = run_delay_svt_event(ex, sensitivity_, epsilon_list, round_, delay_time, tau)
    error_3 = run_discontin_reduce(ex, sensitivity_, epsilon_list, round_, delay_time, tau)
    print(error_1)
    print(error_2)
    print(error_3)
    
    plt.plot(epsilon_list, error_1, label='naive')
    plt.plot(epsilon_list, error_2, label='delay')
    plt.plot(epsilon_list, error_3, label='reduce_noise')
    plt.legend()
    plt.show()