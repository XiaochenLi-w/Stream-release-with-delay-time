import numpy as np
import matplotlib.pyplot as plt

import methods.common_tools
import methods.naive
import methods.sensitivity_calc

def whether_group(groupi, old_avg, new_data, tau, eps_group, sensitivity_):
    total_num = len(groupi)
    #print(total_num)
    new_avg = (old_avg * total_num + new_data) / (total_num + 1)

    dev = 0
    for i in range(total_num):
        dev += abs(groupi[i] - new_avg)

    dev += abs(new_data - new_avg)

    #print(dev / total_num)

    if (dev / total_num) + methods.common_tools.add_noise(sensitivity_ / total_num, eps_group / 4, 1) > tau + methods.common_tools.add_noise(sensitivity_ / total_num, eps_group / 2, 1):
        return 0, new_avg
    else:
        return 1, new_avg
    

#------------orginial pegasus--------------
def pegasus_nodelay(ex, domain_low, domain_high, eps, tau, flag = 0, interval_ = 5, num_ = 100):
    total_time = len(ex)
    dim = len(ex[0])
    eps_group = eps / 5
    eps_pub = eps - eps_group
    published_result = []

    i = 0
    group_ = []
    group_index = []
    group_noisy = []
    avg_ = 0

    whether_update = 0
    sensitivity_ = domain_high
    
    for i in range(total_time):
        if whether_update == 0:
            eps_pub = eps - eps_group
        
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

        if len(group_) == 0:
            group_.append(ex[i][0])
            avg_ = ex[i][0]
            group_index.append(i)
            if ex[i][0] > sensitivity_:
                noisy_result = sensitivity_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
            else:
                noisy_result = ex[i][0] + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)

            published_result.append(noisy_result)
            group_noisy.append(noisy_result)

        else:
            ifadd_, newavg = whether_group(group_, avg_, ex[i][0], tau, eps_group, sensitivity_)
            if ifadd_ == 1:
                group_.append(ex[i][0])
                group_index.append(i)
                avg_ = newavg
                if ex[i][0] > sensitivity_:
                    sum_ = sensitivity_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
                else:
                    sum_ = ex[i][0] + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)

                group_noisy.append(sum_)
                for k in range(len(group_) - 1):
                    sum_ += group_noisy[group_index[k]]
                sum_ = sum_ / len(group_)
                published_result.append(sum_)
            else:
                if ex[i][0] > sensitivity_:
                    noisy_result = sensitivity_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
                else:
                    noisy_result = ex[i][0] + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)

                published_result.append(noisy_result)
                group_noisy.append(noisy_result)
                group_ = []
                group_index = []

    #print(published_result)
    return published_result

#---------pegasus with delay, post-processing------------
def pegasus_delay(ex, domain_low, domain_high, eps, tau, flag = 0, interval_ = 5, num_ = 100):
    total_time = len(ex)
    dim = len(ex[0])
    eps_group = eps / 5
    eps_pub = eps - eps_group
    published_result = []

    i = 0
    group_ = []
    group_index = []
    avg_ = 0

    whether_update = 0
    sensitivity_ = domain_high
    
    for i in range(total_time):
        if whether_update == 0:
            eps_pub = eps - eps_group
        
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

        if len(group_) == 0:
            group_.append(ex[i][0])
            avg_ = ex[i][0]
            group_index.append(i)

        else:
            ifadd_, newavg = whether_group(group_, avg_, ex[i][0], tau, eps_group, sensitivity_)
            if ifadd_ == 1:
                group_.append(ex[i][0])
                avg_ = newavg
            else:
                sum_ = 0
                for k in range(len(group_)):
                    if group_[k] > sensitivity_:
                        sum_ += sensitivity_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
                    else:
                        sum_ += group_[k] + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)

                sum_ = sum_ / len(group_)
                for k in range(len(group_)):
                    published_result.append(sum_)

                noisy_result = ex[i][0] + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
                published_result.append(noisy_result)
                group_ = []

    if len(published_result) < total_time:
        sum_ = 0
        for k in range(len(group_)):
            if group_[k] > sensitivity_:
                sum_ += sensitivity_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
            else:
                sum_ += group_[k] + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)

        sum_ = sum_ / len(group_)
        for k in range(len(group_)):
            published_result.append(sum_)
    #print(published_result)
    return published_result

#---------continuous, noisy reduce------------
def reduce_noise_continuous(ex, domain_low, domain_high, eps, tau, delay_time, flag = 0, interval_ = 5):
    total_time = len(ex)
    dim = len(ex[0])
    eps_group = eps / 5
    eps_pub = eps - eps_group
    published_result = []

    i = 0
    group_ = []
    avg_ = 0
    
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

        if i % delay_time == 0 and len(group_) != 0:
            sum_ = 0
            for k in range(len(group_)):
                if group_[k] > sensitivity_:
                    sum_ += sensitivity_
                else:
                    sum_ += group_[k]

            sum_ = (sum_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
            for k in range(len(group_)):
                published_result.append(sum_)
            group_ = [] 

        if len(group_) == 0:
            group_.append(ex[i][0])
            avg_ = ex[i][0]

        else:
            ifadd_, newavg = whether_group(group_, avg_, ex[i][0], tau, eps_group, sensitivity_)
            if ifadd_ == 1:
                group_.append(ex[i][0])
                avg_ = newavg
            else:
                sum_ = 0
                for k in range(len(group_)):
                    if group_[k] > sensitivity_:
                        sum_ += sensitivity_
                    else:
                        sum_ += group_[k]
                sum_ = (sum_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
                for k in range(len(group_)):
                    published_result.append(sum_)

                noisy_result = ex[i][0] + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)
                published_result.append(noisy_result)
                group_ = []

    if len(published_result) < total_time:
        sum_ = 0
        for k in range(len(group_)):
            if group_[k] > sensitivity_:
                sum_ += sensitivity_
            else:
                sum_ += group_[k]

        sum_ = (sum_ + methods.common_tools.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
        for k in range(len(group_)):
            published_result.append(sum_)
    #print(published_result)
    return published_result


def run_pegasus_nodelay(ex, domain_low, domain_high, epsilon_list, round_, tau, flag = 0, interval_ = 5, num_ = 100):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = pegasus_nodelay(ex, domain_low, domain_high, eps, tau, flag, interval_, num_)
            err_round += methods.common_tools.count_mae(ex, published_result)

        error_.append(err_round / round_)

    print('PeGaSus:', error_)

    return error_


def run_pegasus_delay(ex, domain_low, domain_high, epsilon_list, round_, tau, flag = 0, interval_ = 5, num_ = 100):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = pegasus_delay(ex, domain_low, domain_high, eps, tau, flag, interval_, num_)
            err_round += methods.common_tools.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('PeGaSus_Delay:', error_)

    return error_


def run_reduce_noise_continuous(ex, domain_low, domain_high, epsilon_list, round_, tau, delay_time, flag = 0, interval_ = 5):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = reduce_noise_continuous(ex, domain_low, domain_high, eps, tau, delay_time, flag, interval_)
            err_round += methods.common_tools.count_mae(ex, published_result)

        error_.append(err_round / round_)

    print('Contin_reduce:', error_)

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
    tau = 3
    #sensitivity_ = 1
    delay_time = 100

    error_1 = naive.run_naive_event(ex, max(data), epsilon_list, round_)
    error_2 = run_pegasus_delay(ex, min(data), max(data), epsilon_list, round_, tau, 1, 2)
    error_3 = run_pegasus_nodelay(ex, min(data), max(data), epsilon_list, round_, tau, 1, 2)
    error_4 = run_reduce_noise_continuous(ex, min(data), max(data), epsilon_list, round_, tau, delay_time, 1, 2)
    print(error_1)
    print(error_2)
    print(error_3)
    
    plt.plot(epsilon_list, error_1, label='naive')
    plt.plot(epsilon_list, error_2, label='pegasus_delay')
    plt.plot(epsilon_list, error_3, label='pegasus_nodelay')
    plt.plot(epsilon_list, error_4, label='continuous_reduce')
    plt.legend()
    plt.show()