import numpy as np
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

def whether_group(groupi, old_avg, new_data, tau, eps_group, sensitivity_):
    total_num = len(groupi)
    #print(total_num)
    new_avg = (old_avg * total_num + new_data) / (total_num + 1)

    dev = 0
    for i in range(total_num):
        dev += abs(groupi[i] - new_avg)

    dev += abs(new_data - new_avg)

    #print(dev / total_num)

    if (dev / total_num) + delay_spas.add_noise(sensitivity_ / total_num, eps_group / 4, 1) > tau + delay_spas.add_noise(sensitivity_ / total_num, eps_group / 2, 1):
        return 0, new_avg
    else:
        return 1, new_avg


#----------continuous grouping in sliding, reduce added noise---------
def reduce_noise_delay(ex, sensitivity_, eps, tau, delay_time):
    total_time = len(ex)
    dim = len(ex[0])
    eps_pub = 3 * eps / 4
    eps_group = eps - eps_pub
    published_result = []

    i = 0
    group_ = []
    group_index = []
    avg_ = 0
    flag_ = False

    delay_count = 0
    
    for i in range(total_time - delay_time + 1):
        
        if i == 0:
            group_.append(ex[0][0])
            avg_ = ex[i][0]
            group_index.append(i)
            delay_count += 1

            for j in range(i + 1, i + delay_time):
                if len(group_) == 0:
                    group_.append(ex[j][0])
                    group_index.append(j)
                    avg_ = ex[j][0]
                    delay_count += 1
                    continue

                ifadd_, newavg = whether_group(group_, avg_, ex[j][0], tau, eps_group, sensitivity_)
                if ifadd_ == 1:
                    group_.append(ex[j][0])
                    group_index.append(j)
                    avg_ = newavg
                    delay_count += 1
                else:
                    # close the current group
                    sum_ = 0
                    for k in range(len(group_)):
                        sum_ += group_[k]
                    noisy_value = (sum_ + delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
                    for k in range(len(group_)):
                        published_result.append(noisy_value)

                    # the current value is a new group
                    noisy_value = ex[j][0] + delay_spas.add_noise(sensitivity_, eps_pub, dim)
                    published_result.append(noisy_value)
                    # start a new group
                    group_ = []
                    group_index = []
                    flag_ = False
                    delay_count = 0
    
        else:
            if len(group_) == 0:
                group_.append(ex[i + delay_time - 1][0])
                group_index.append(i + delay_time - 1)
                avg_ = ex[i + delay_time - 1][0]
                delay_count += 1
                if i + delay_time == total_time:
                    published_result.append(ex[i + delay_time - 1][0] + delay_spas.add_noise(sensitivity_, eps_pub, dim))
                continue

            # if it is the last delay time window, release all the remaining data in group
            if i + delay_time <= total_time:
                #print('##', i+delay_time-1)

                # for the following delay time window, there is only one new value need to be calculate after sliding
                ifadd_, newavg = whether_group(group_, avg_, ex[i + delay_time - 1][0], tau, eps_group, sensitivity_)
                if ifadd_ == 1:
                        group_.append(ex[i + delay_time - 1][0])
                        group_index.append(i + delay_time - 1)
                        avg_ = newavg
                        delay_count += 1
                        if delay_count > delay_time:
                            sum_noisy = 0
                            sum_new = 0
                            for idex, k in enumerate(group_index):
                                if k > len(published_result) - 1:
                                    sum_new += group_[idex]
                                else:
                                    sum_noisy += published_result[k]
                            noisy_value = (sum_noisy + sum_new + delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
                            for k in range(len(published_result), group_index[-1] + 1):
                                published_result.append(noisy_value)
                            delay_count = 0
                            flag_ = True
                else:
                    # if there are part of value have been released, add their noisy value
                    if flag_:
                        sum_noisy = 0
                        sum_new = 0
                        for idex, k in enumerate(group_index):
                            if k > len(published_result) - 1:
                                sum_new += group_[idex]
                            else:
                                sum_noisy += published_result[k]
                        noisy_value = (sum_noisy + sum_new + delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
                        for k in range(len(published_result), group_index[-1] + 1):
                            published_result.append(noisy_value)
                    # if all the values in group haven't been released, add their original value and add noise
                    else:
                        sum_ = 0
                        for k in range(len(group_)):
                            sum_ += group_[k]
                        noisy_value = (sum_ + delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
                        for k in range(len(group_)):
                            published_result.append(noisy_value)
                        #print(len(published_result))

                    # the current value is a new group
                    noisy_value = ex[i + delay_time - 1][0] + delay_spas.add_noise(sensitivity_, eps_pub, dim)
                    published_result.append(noisy_value)
                    # start a new group
                    group_ = []
                    group_index = []
                    flag_ = False
                    delay_count = 0

       #print(i)
        if (i + delay_time == total_time) and delay_count > 0:

            #print('inner_before:', i + delay_time, len(published_result))
            if flag_:
                sum_noisy = 0
                sum_new = 0
                for idex, k in enumerate(group_index):
                    if k > len(published_result) - 1:
                        sum_new += group_[idex]
                    else:
                        sum_noisy += published_result[k]
                noisy_value = (sum_noisy + sum_new + delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
                for k in range(len(published_result), group_index[-1] + 1):
                    published_result.append(noisy_value)
            else:
                sum_ = 0
                for k in range(len(group_)):
                    sum_ += group_[k]
                noisy_value = (sum_ + delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
                for k in range(len(group_)):
                    published_result.append(noisy_value)

                flag_ = True
            
            #print('inner_after:', i + delay_time, len(published_result))

    #print(published_result)
    return published_result


#----------continuous grouping in sliding, close when delay time run out, reduce added noise---------
def reduce_noise_delayclose(ex, sensitivity_, eps, tau, delay_time):
    total_time = len(ex)
    dim = len(ex[0])
    eps_pub = 3 * eps / 4
    eps_group = eps - eps_pub
    published_result = []

    i = 0
    group_ = []
    group_index = []
    avg_ = 0

    delay_count = 0
    
    for i in range(total_time - delay_time + 1):
        
        if i == 0:
            group_.append(ex[0][0])
            avg_ = ex[i][0]
            group_index.append(i)
            delay_count += 1

            for j in range(i + 1, i + delay_time):
                if len(group_) == 0:
                    group_.append(ex[j][0])
                    group_index.append(j)
                    avg_ = ex[j][0]
                    delay_count += 1
                    continue

                ifadd_, newavg = whether_group(group_, avg_, ex[j][0], tau, eps_group, sensitivity_)
                if ifadd_ == 1:
                    group_.append(ex[j][0])
                    group_index.append(j)
                    avg_ = newavg
                    delay_count += 1
                else:
                    # close the current group
                    sum_ = 0
                    for k in range(len(group_)):
                        sum_ += group_[k]
                    noisy_value = (sum_ + delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
                    for k in range(len(group_)):
                        published_result.append(noisy_value)

                    # the current value is a new group
                    noisy_value = ex[j][0] + delay_spas.add_noise(sensitivity_, eps_pub, dim)
                    published_result.append(noisy_value)
                    # start a new group
                    group_ = []
                    group_index = []
                    flag_ = False
                    delay_count = 0
    
        else:
            if len(group_) == 0:
                group_.append(ex[i + delay_time - 1][0])
                group_index.append(i + delay_time - 1)
                avg_ = ex[i + delay_time - 1][0]
                delay_count += 1
                if i + delay_time == total_time:
                    published_result.append(ex[i + delay_time - 1][0] + delay_spas.add_noise(sensitivity_, eps_pub, dim))
                continue

            # if it is the last delay time window, release all the remaining data in group
            if i + delay_time <= total_time:
                #print('##', i+delay_time-1)

                # for the following delay time window, there is only one new value need to be calculate after sliding
                ifadd_, newavg = whether_group(group_, avg_, ex[i + delay_time - 1][0], tau, eps_group, sensitivity_)
                if ifadd_ == 1:
                        group_.append(ex[i + delay_time - 1][0])
                        group_index.append(i + delay_time - 1)
                        avg_ = newavg
                        delay_count += 1
                        if delay_count > delay_time:
                            sum_ = 0
                            for k in range(len(group_)):
                                sum_ += group_[k]
                            noisy_value = (sum_ + delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
                            for k in range(len(group_)):
                                published_result.append(noisy_value)

                            group_ = []
                            group_index = []
                            delay_count = 0

                else:             
                    sum_ = 0
                    for k in range(len(group_)):
                        sum_ += group_[k]
                    noisy_value = (sum_ + delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
                    for k in range(len(group_)):
                        published_result.append(noisy_value)
                    #print(len(published_result))

                    # the current value is a new group
                    noisy_value = ex[i + delay_time - 1][0] + delay_spas.add_noise(sensitivity_, eps_pub, dim)
                    published_result.append(noisy_value)
                    # start a new group
                    group_ = []
                    group_index = []
                    delay_count = 0

       #print(i)
        if (i + delay_time == total_time) and delay_count > 0:

            #print('inner_before:', i + delay_time, len(published_result))
            sum_ = 0
            for k in range(len(group_)):
                sum_ += group_[k]
            noisy_value = (sum_ + delay_spas.add_noise(sensitivity_, eps_pub, dim)) / len(group_)
            for k in range(len(group_)):
                published_result.append(noisy_value)
     
            #print('inner_after:', i + delay_time, len(published_result))

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


def run_reduce_noise_delay(ex, sensitivity_, epsilon_list, round_, tau, delay_time):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = reduce_noise_delay(ex, sensitivity_, eps, tau, delay_time)
            err_round += count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_



def run_reduce_noise_delayclose(ex, sensitivity_, epsilon_list, round_, tau, delay_time):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = reduce_noise_delayclose(ex, sensitivity_, eps, tau, delay_time)
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

    round_ = 1
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    tau = 3
    sensitivity_ = max(data) - min(data)
    #sensitivity_ = 1
    delay_time = 10

    error_1 = run_naive_event(ex, sensitivity_, epsilon_list, round_)
    error_2 = run_reduce_noise_delay(ex, sensitivity_, epsilon_list, round_, tau, delay_time)
    error_3 = run_reduce_noise_delayclose(ex, sensitivity_, epsilon_list, round_, tau, delay_time)
    print(error_1)
    print(error_2)
    print(error_3)
    
    plt.plot(epsilon_list, error_1, label='naive')
    plt.plot(epsilon_list, error_2, label='reduce_noise')
    plt.plot(epsilon_list, error_3, label='reduce_noiseclose')
    plt.legend()
    plt.show()