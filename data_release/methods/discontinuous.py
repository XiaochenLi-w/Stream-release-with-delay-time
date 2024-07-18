import numpy as np
import matplotlib.pyplot as plt

import methods.common_tools
import methods.naive
import methods.sensitivity_calc

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

    if (dev / total_num) + methods.common_tools.add_noise(sensitivity_ / total_num, eps_group / (4 * (2 * delay_time - 1)), 1) > tau + methods.common_tools.add_noise(sensitivity_ / total_num, eps_group / (2 * (2 * delay_time - 1)), 1):
        return 0, new_avg
    else:
        return 1, new_avg
    
    #------------discontinuous grouping in batch with post-processing-------------
def delay_discontin_post(ex, domain_low, domain_high, eps, delay_time, tau, flag = 0, interval_ = 5):
    total_time = len(ex)
    dim = len(ex[0])
    eps_group = eps / 5
    eps_pub = eps - eps_group
    published_result = []

    i = 0
    whether_update = 0
    sensitivity_ = domain_high
    
    for i in range(total_time):
        if whether_update == 0:
            eps_pub = eps - eps_group

        if i % delay_time == 0:
            if (i / delay_time) % interval_ == 0 and flag == 1 and (i + 1) * delay_time <= total_time:
                eps_s = eps_pub / 2
                eps_pub = eps_pub - eps_s

                data_sens = np.zeros(delay_time, dtype = int)
                cc = 0
                for qq in range(i * delay_time, (i + 1) * delay_time):
                    data_sens[cc] = ex[qq][0]
                    cc += 1

                sensitivity_ = methods.sensitivity_calc.quality_func(data_sens, domain_low, domain_high, interval_, eps_s)
                whether_update = 1
            else:
                whether_update = 0

            if i > 0:
                results_indelay = np.zeros(delay_time, dtype=float)
                for j in range(len(group_)):
                    sum_ = 0
                    for k in range(len(group_[j])):
                        if group_[j][k] > sensitivity_:
                            sum_ += sensitivity_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
                        else:
                            sum_ += group_[j][k] + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)

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
                        if group_[j][k] > sensitivity_:
                            sum_ += sensitivity_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
                        else:
                            sum_ += group_[j][k] + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)

                    sum_ = sum_ / len(group_[j])
                    for k in range(len(group_[j])):
                        index = group_index[j][k]
                        results_indelay[index % delay_time] = sum_
        
                for j in results_indelay:
                    published_result.append(j)

    #print(published_result)
    return published_result


#------------discontinuous grouping in batch with reduce noise-------------
def discontin_reduce(ex, domain_low, domain_high, eps, delay_time, tau, flag = 0, interval_ = 5):
    total_time = len(ex)
    dim = len(ex[0])
    eps_pub =4 * eps / 5
    eps_group = eps - eps_pub
    published_result = []

    i = 0
    whether_update = 0
    sensitivity_ = domain_high
    
    for i in range(total_time):
        if whether_update == 0:
            eps_pub = eps - eps_group

        if i % delay_time == 0:
            if (i / delay_time) % interval_ == 0 and flag == 1 and (i + 1) * delay_time <= total_time:
                eps_s = eps_pub / 2
                eps_pub = eps_pub - eps_s

                data_sens = np.zeros(delay_time, dtype = int)
                cc = 0
                for qq in range(i * delay_time, (i + 1) * delay_time):
                    data_sens[cc] = ex[qq][0]
                    cc += 1

                sensitivity_ = methods.sensitivity_calc.quality_func(data_sens, domain_low, domain_high, interval_, eps_s)
                whether_update = 1
            else:
                whether_update = 0

            if i > 0:
                results_indelay = np.zeros(delay_time, dtype=float)
                for j in range(len(group_)):
                    sum_ = 0
                    for k in range(len(group_[j])):
                        if group_[j][k] > sensitivity_:
                            sum_ += sensitivity_
                        else:
                            sum_ += group_[j][k]

                    sum_ = (sum_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)) / len(group_[j])
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
                        if group_[j][k] > sensitivity_:
                            sum_ += sensitivity_
                        else:
                            sum_ += group_[j][k]

                    sum_ = (sum_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)) / len(group_[j])
                    for k in range(len(group_[j])):
                        index = group_index[j][k]
                        results_indelay[index % delay_time] = sum_
        
                for j in results_indelay:
                    published_result.append(j)

    #print(published_result)
    return published_result


def run_discontin_post(ex, domain_low, domain_high, epsilon_list, round_, delay_time, tau, flag = 0, interval_ = 5):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = delay_discontin_post(ex, domain_low, domain_high, eps, delay_time, tau, flag, interval_)
            err_round += methods.common_tools.count_mae(ex, published_result)

        error_.append(err_round / round_)

    print('Discontin_pp:', error_)

    return error_

def run_discontin_reduce(ex, domain_low, domain_high, epsilon_list, round_, delay_time, tau, flag = 0, interval_ = 5):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = discontin_reduce(ex, domain_low, domain_high, eps, delay_time, tau, flag, interval_)
            err_round += methods.common_tools.count_mae(ex, published_result)

        error_.append(err_round / round_)

    print('Discontin_reduce:', error_)

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

    filename = "./data/COVID19 DEATH.csv"
    with open(filename, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')
                
                ex.append([int(float(tmp[-1]))])
    
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
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    delay_time = 100
    tau = 3
    
    error_1 = naive.run_naive_event(ex, max(data), epsilon_list, round_)
    error_2 = run_discontin_post(ex, min(data), max(data), epsilon_list, round_, delay_time, tau, 1)
    error_3 = run_discontin_reduce(ex, min(data), max(data), epsilon_list, round_, delay_time, tau, 1)
    print(error_1)
    print(error_2)
    print(error_3)
    
    plt.plot(epsilon_list, error_1, label='naive')
    plt.plot(epsilon_list, error_2, label='post')
    plt.plot(epsilon_list, error_3, label='reduce_noise')
    plt.legend()
    plt.show()