import numpy as np
import matplotlib.pyplot as plt

import event_post
import non_slide
import pegasus
import reduce_noise
import order_adv

# -------naive----------
def run_naive_event(ex, sensitivity_, epsilon_list, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = non_slide.naive_event(ex, sensitivity_, eps)
            err_round += non_slide.count_mae(ex, published_result)
            #print('round', j, 'over!')

        error_.append(err_round / round_)
    
    print('naive:', error_)
    return error_


# ------Order-based-------
def run_delay_svt_event(ex, sensitivity_, epsilon_list, round_, delay_time):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = event_post.delay_svt_event(ex, sensitivity_, eps, delay_time)
            err_round += event_post.count_mae(ex, published_result)
            #print('round', j, 'over!')

        error_.append(err_round / round_)
    
    print('Order_based:', error_)
    return error_


# -------discontin + post-processing + in batch---------
def run_delay_group_event(ex, sensitivity_, epsilon_list, round_, delay_time, tau):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = non_slide.delay_noslide_event(ex, sensitivity_, eps, delay_time, tau)
            err_round += non_slide.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('discontin_pp:', error_)
    return error_


# --------discontin + noise reduce + in batch------------
def run_discontin_reduce(ex, sensitivity_, epsilon_list, round_, delay_time, tau):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = non_slide.discontin_reduce(ex, sensitivity_, eps, delay_time, tau)
            err_round += non_slide.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('discontin_reduce:', error_)
    return error_


# -----------Orginial PeGaSus: contin + post-processing + sliding------------
def run_pegasus_event(ex, sensitivity_, epsilon_list, round_, tau):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = pegasus.pegasus_nodelay(ex, sensitivity_, eps, tau)
            err_round += pegasus.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('pegasus:', error_)
    return error_


# ---------PeGaSus with delay: contin + post-processing + sliding------------
def run_pegasus_delay(ex, sensitivity_, epsilon_list, round_, tau):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = pegasus.pegasus_delay(ex, sensitivity_, eps, tau)
            err_round += pegasus.count_mae(ex, published_result)

        error_.append(err_round / round_)

    print('PeGaSus_delaypp:', error_)
    return error_


# -------contin + noise reduce + sliding + no close when publish-----------
def run_reduce_noise_delay(ex, sensitivity_, epsilon_list, round_, tau, delay_time):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = reduce_noise.reduce_noise_delay(ex, sensitivity_, eps, tau, delay_time)
            err_round += reduce_noise.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('contin_noisered:', error_)
    return error_


# -------contin + noise reduce + sliding + close when publish-----------
def run_reduce_noise_delayclose(ex, sensitivity_, epsilon_list, round_, tau, delay_time):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = reduce_noise.reduce_noise_delayclose(ex, sensitivity_, eps, tau, delay_time)
            err_round += reduce_noise.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('contin_noisered_close:', error_)
    return error_


# -------order_advance------------
def run_order_advance(ex, sensitivity_, epsilon_list, round_, delay_time, buc_size):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = order_adv.order_advance(ex, sensitivity_, eps, delay_time, buc_size)
            err_round += order_adv.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('order_adv:', error_)
    return error_

if __name__ == "__main__":

    ex = []
    filename = []
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

    # data = np.zeros(len(ex), dtype=int)
    # for i in range(len(ex)):
    #     data[i] = ex[i][0]
    
    count = 0
    ex1 = []
    #filename1 = "./data/COVID19 DEATH.csv"
    filename1 = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/COVID19 DEATH.csv"
    with open(filename1, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')
                
                ex1.append([int(float(tmp[-1]))])
    ex.append(ex1)
    filename.append(filename1)
    
    # count = 0
    # ex2 = []
    # #filename2 = "./data/INFLUENZA DEATHS.csv"
    # filename2 = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/INFLUENZA DEATHS.csv"
    # with open(filename2, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 3:
    #             tmp = lines.split(',')
                
    #             ex2.append([int(float(tmp[-1]))])
    # ex.append(ex2)
    # filename.append(filename2)

    # count = 0
    # ex3 = []
    # #filename3 = "./data/PNEUMONIA DEATHS.csv"
    # filename3 = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/PNEUMONIA DEATHS.csv"
    # with open(filename3, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 3:
    #             tmp = lines.split(',')
                
    #             ex3.append([int(float(tmp[-1]))])
    # ex.append(ex3)
    # filename.append(filename3)

    # count = 0
    # ex4 = []
    # #filename4 = "./data/TOTAL DEATH.csv"
    # filename4 = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/TOTAL DEATH.csv"
    # with open(filename4, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 3:
    #             tmp = lines.split(',')
                
    #             ex4.append([int(float(tmp[-1]))])
    # ex.append(ex4)
    # filename.append(filename4)
 
    count = 0
    ex5 = []
    #filename5 = "./data/National_Custom_Data.csv"
    filename5 = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/National_Custom_Data.csv"
    with open(filename5, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')
                
                ex5.append([int(float(tmp[-2]))])
    ex.append(ex5)
    filename.append(filename5)
    
    count = 0
    ex7 = []
    #filename7 = "./data/unemployment.csv"
    filename7 = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/unemployment.csv"
    with open(filename7, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')        
                ex7.append([int(tmp[-1])])

    ex.append(ex7)
    filename.append(filename7)

    for k in range(len(ex)):
        print('#It is the results of', filename[k])

        length_ = len(ex[k])
        data = np.zeros(length_, dtype=int)
        for i in range(length_):
            data[i] = ex[k][i][0]

        round_ = 20
        #epsilon_list = [0.00001, 0.00002, 0.00003, 0.00004, 0.00005]
        epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        delay_time = 100
        tau = 3
        sensitivity_ = max(data) - min(data)
        #print(sensitivity_)
        #sensitivity_ = 1

        error_naive = run_naive_event(ex[k], sensitivity_, epsilon_list, round_)
        error_order = run_delay_svt_event(ex[k], sensitivity_, epsilon_list, round_, delay_time)
        error_group = run_delay_group_event(ex[k], sensitivity_, epsilon_list, round_, delay_time, tau)
        error_pegasus_delay = run_pegasus_delay(ex[k], sensitivity_, epsilon_list, round_, tau)
        error_pegasus_nodelay = run_pegasus_event(ex[k], sensitivity_, epsilon_list, round_, tau)
        error_reduce_noise = run_reduce_noise_delay(ex[k], sensitivity_, epsilon_list, round_, tau, delay_time)
        error_reduce_noiseclose = run_reduce_noise_delayclose(ex[k], sensitivity_, epsilon_list, round_, tau, delay_time)
        error_disgroup_reduce = run_discontin_reduce(ex[k], sensitivity_, epsilon_list, round_, delay_time, tau)
        error_order_advance = run_order_advance(ex[k], sensitivity_, epsilon_list, round_, delay_time, 20)
    
        # plt.plot(epsilon_list, error_naive, label='naive')
        # #plt.plot(epsilon_list, error_order, label='order')
        # plt.plot(epsilon_list, error_group, label='group')
        # plt.plot(epsilon_list, error_pegasus_delay, label='pegasus_delay')
        # plt.plot(epsilon_list, error_pegasus_nodelay, label='pegasus_nodelay')
        # plt.plot(epsilon_list, error_reduce_noise, label='reduce_noise')
        # plt.plot(epsilon_list, error_reduce_noiseclose, label='reduce_noise_delayclose')
        # plt.plot(epsilon_list, error_order_advance, label='order_advance')
        # plt.legend()
        # plt.show()