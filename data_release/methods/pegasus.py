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

def whether_group(groupi, old_avg, new_data, tau, eps_group, sensitivity_):
    total_num = len(groupi)
    #print(total_num)
    new_avg = (old_avg * total_num + new_data) / (total_num + 1)

    dev = 0
    for i in range(total_num):
        dev += abs(groupi[i] - new_avg)

    dev += abs(new_data - new_avg)

    #print(dev / total_num)

    if (dev / total_num) + methods.delay_spas.add_noise(sensitivity_ / total_num, eps_group / 4, 1) > tau + methods.delay_spas.add_noise(sensitivity_ / total_num, eps_group / 2, 1):
        return 0, new_avg
    else:
        return 1, new_avg

#---------pegasus with delay, post-processing------------
def pegasus_delay(ex, sensitivity_, eps, tau):
    total_time = len(ex)
    dim = len(ex[0])
    eps_pub =3 * eps / 4
    eps_group = eps - eps_pub
    published_result = []

    i = 0
    group_ = []
    group_index = []
    avg_ = 0
    
    for i in range(total_time):
        if len(group_) == 0:
            group_.append(ex[i][0])
            avg_ = ex[i][0]
            group_index.append(i)
            #published_result.append(ex[i][0] + delay_spas.add_noise(sensitivity_, eps, dim))

        else:
            ifadd_, newavg = whether_group(group_, avg_, ex[i][0], tau, eps_group, sensitivity_)
            if ifadd_ == 1:
                group_.append(ex[i][0])
                avg_ = newavg
                # sum_ = ex[i][0] + delay_spas.add_noise(sensitivity_, eps_pub, dim)
                # for k in range(len(group_) - 1):
                #     sum_ += published_result[group_index[k]]
                # sum_ = sum_ / len(group_)
                # published_result.append(sum_)
            else:
                sum_ = 0
                for k in range(len(group_)):
                    sum_ += group_[k] + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)
                sum_ = sum_ / len(group_)
                for k in range(len(group_)):
                    published_result.append(sum_)

                noisy_result = ex[i][0] + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)
                published_result.append(noisy_result)
                group_ = []
                #published_result.append(ex[i][0] + delay_spas.add_noise(sensitivity_, eps_pub, dim))
    if len(published_result) < total_time:
        sum_ = 0
        for k in range(len(group_)):
            sum_ += group_[k] + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)
        sum_ = sum_ / len(group_)
        for k in range(len(group_)):
            published_result.append(sum_)
    #print(published_result)
    return published_result

#------------orginial pegasus--------------
def pegasus_nodelay(ex, sensitivity_, eps, tau):
    total_time = len(ex)
    dim = len(ex[0])
    eps_pub =4 * eps / 5
    eps_group = eps - eps_pub
    published_result = []

    i = 0
    group_ = []
    group_index = []
    group_noisy = []
    avg_ = 0
    
    for i in range(total_time):
        if len(group_) == 0:
            group_.append(ex[i][0])
            avg_ = ex[i][0]
            group_index.append(i)
            noisy_result = ex[i][0] + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)
            published_result.append(noisy_result)
            group_noisy.append(noisy_result)

        else:
            ifadd_, newavg = whether_group(group_, avg_, ex[i][0], tau, eps_group, sensitivity_)
            if ifadd_ == 1:
                group_.append(ex[i][0])
                group_index.append(i)
                avg_ = newavg
                sum_ = ex[i][0] + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)
                group_noisy.append(sum_)
                for k in range(len(group_) - 1):
                    sum_ += group_noisy[group_index[k]]
                sum_ = sum_ / len(group_)
                published_result.append(sum_)
            else:
                noisy_result = ex[i][0] + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)
                published_result.append(noisy_result)
                group_noisy.append(noisy_result)
                group_ = []
                group_index = []

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


def run_pegasus_event(ex, sensitivity_, epsilon_list, round_, tau):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = pegasus_delay(ex, sensitivity_, eps, tau)
            err_round += count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_

def run_pegasus_nodelay(ex, sensitivity_, epsilon_list, round_, tau):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = pegasus_nodelay(ex, sensitivity_, eps, tau)
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

    error_1 = run_naive_event(ex, sensitivity_, epsilon_list, round_)
    error_2 = run_pegasus_event(ex, sensitivity_, epsilon_list, round_, tau)
    error_3 = run_pegasus_nodelay(ex, sensitivity_, epsilon_list, round_, tau)
    print(error_1)
    print(error_2)
    print(error_3)
    
    plt.plot(epsilon_list, error_1, label='naive')
    plt.plot(epsilon_list, error_2, label='pegasus_delay')
    plt.plot(epsilon_list, error_3, label='pegasus_nodelay')
    plt.legend()
    plt.show()