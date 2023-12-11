#----------Order-based-------------
import numpy as np
import methods.delay_spas
import matplotlib.pyplot as plt

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

def naive_event(ex, sensitivity_, eps):
    total_time = len(ex)
    dim = len(ex[0])

    published_result = []

    for i in range(total_time):
        noise_result = ex[i][0] + methods.delay_spas.add_noise(sensitivity_, eps, dim)
        published_result.append(noise_result)

    return published_result

#-----------Order-based------------
def delay_svt_event(ex, sensitivity_, eps, delay_time):
    total_time = len(ex)
    dim = len(ex[0])
    eps_post = eps / 4
    eps_pub = eps - eps_post
    eps_1 = eps_post / 2
    eps_2 = eps_post / 2

    published_result = []
    flag_ = []

    rho_ = methods.delay_spas.add_noise(sensitivity_, eps_1 / 2, dim)

    for i in range(total_time):

        noise_result = ex[i][0] + methods.delay_spas.add_noise(sensitivity_, eps_pub, dim)

        temp = []
        if i + delay_time < total_time:
            for j in range(i + 1, i + delay_time):
                if ex[i][0] - ex[j][0] + methods.delay_spas.add_noise(sensitivity_, eps_2 / (2 * (2 * delay_time - 1)), dim) > rho_:
                #if ex[i][0] - ex[j][0] > 0:
                    temp.append(0)
                else:
                    temp.append(1)
        elif i + 1 < total_time:
            for j in range(i + 1, total_time):
                if ex[i][0] - ex[j][0] + methods.delay_spas.add_noise(sensitivity_, eps_2 / (2 * (2 * delay_time - 1)), dim) > rho_:
                #if ex[i][0] - ex[j][0] > 0:
                    temp.append(0)
                else:
                    temp.append(1)
        else:
            temp = []
        
        flag_.append(temp)
        
        low_ = 0
        high_ = 10000
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
        
        # if low_ > high_:
        #         if noise_result > low_:
        #             noise_result = low_
        #         elif noise_result < high_:
        #             noise_result = high_
        if noise_result > low_ or noise_result < high_:
            if low_ > high_:
                noise_result = (low_ + high_) / 2

        published_result.append(noise_result)

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


def run_delay_svt_event(ex, sensitivity_, epsilon_list, round_, delay_time):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = delay_svt_event(ex, sensitivity_, eps, delay_time)
            err_round += count_mae(ex, published_result)
            print('round', j, 'over!')

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
    
    data = np.zeros(len(ex), dtype=int)
    for i in range(len(ex)):
        data[i] = ex[i][0]

    round_ = 10
    epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    delay_time = 100
    sensitivity_ = max(data) - min(data)

    error_1 = run_naive_event(ex, sensitivity_, epsilon_list, round_)
    error_2 = run_delay_svt_event(ex, sensitivity_, epsilon_list, round_, delay_time)
    print(error_1)
    print(error_2)
    
    plt.plot(epsilon_list, error_1, label='naive')
    plt.plot(epsilon_list, error_2, label='delay')
    plt.legend()
    plt.show()