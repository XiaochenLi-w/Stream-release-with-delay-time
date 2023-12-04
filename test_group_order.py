import numpy as np
import matplotlib.pyplot as plt

import event_post
import non_slide
import pegasus
import reduce_noise

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
def run_delay_svt_event(ex, sensitivity_, eps, round_, delay_time_list):
    error_ = []
    for delay_time in delay_time_list:
        err_round = 0
        for j in range(round_):
            published_result = event_post.delay_svt_event(ex, sensitivity_, eps, delay_time)
            err_round += event_post.count_mae(ex, published_result)
            #print('round', j, 'over!')

        error_.append(err_round / round_)
    
    print('Order_based:', error_)
    return error_


# -------discontin + post-processing + in batch---------
def run_delay_group_event(ex, sensitivity_, eps, round_, delay_time_list, tau):
    error_ = []
    for delay_time in delay_time_list:
        err_round = 0
        for j in range(round_):
            published_result = non_slide.delay_noslide_event(ex, sensitivity_, eps, delay_time, tau)
            err_round += non_slide.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('discontin_pp:', error_)
    return error_


# --------discontin + noise reduce + in batch------------
def run_discontin_reduce(ex, sensitivity_, eps, round_, delay_time_list, tau):
    error_ = []
    for delay_time in delay_time_list:
        err_round = 0
        for j in range(round_):
            published_result = non_slide.discontin_reduce(ex, sensitivity_, eps, delay_time, tau)
            err_round += non_slide.count_mae(ex, published_result)

        error_.append(err_round / round_)
    
    print('discontin_reduce:', error_)
    return error_

if __name__ == "__main__":

    ex = []
    filename = []

    # count = 0
    # ex1 = []
    # filename1 = "./data/COVID19 DEATH.csv"
    # with open(filename1, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 3:
    #             tmp = lines.split(',')
                
    #             ex1.append([int(float(tmp[-1]))])
    # ex.append(ex1)
    # filename.append(filename1)
    

    count = 0
    ex7 = []
    filename7 = "./data/unemployment.csv"
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


    # count = 0
    # ex5 = []
    # filename5 = "./data/National_Custom_Data.csv"
    # with open(filename5, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 3:
    #             tmp = lines.split(',')
                
    #             ex5.append([int(float(tmp[-2]))])
    # ex.append(ex5)
    # filename.append(filename5)
    
    # count = 0
    # ex1 = []
    
    # count = 0
    # ex5 = []
    # filename5 = "./data/synthetic/increase.csv"
    # with open(filename5, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 3:
    #             tmp = lines.split(',')
                
    #             ex5.append([int(float(tmp[-1]))])
    # ex.append(ex5)
    # filename.append(filename5)
    
    for k in range(len(ex)):
        print('#It is the results of', filename[k])

        length_ = len(ex[k])
        data = np.zeros(length_, dtype=int)
        for i in range(length_):
            data[i] = ex[k][i][0]

        round_ = 20
        #epsilon_list = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005]
        #epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        epsilon = 0.5
        # delay_time = 10
        delay_time_list = [10, 30, 50, 70, 90]
        tau = 3
        sensitivity_ = max(data) - min(data)
        #print(sensitivity_)
        #sensitivity_ = 1

        #error_naive = run_naive_event(ex[k], sensitivity_, epsilon, round_)
        error_order = run_delay_svt_event(ex[k], sensitivity_, epsilon, round_, delay_time_list)
        error_group = run_delay_group_event(ex[k], sensitivity_, epsilon, round_, delay_time_list, tau)
        error_disgroup_reduce = run_discontin_reduce(ex[k], sensitivity_, epsilon, round_, delay_time_list, tau)

        #plt.plot(delay_time_list, error_naive, label='naive')
        plt.plot(delay_time_list, error_order, label='order')
        plt.plot(delay_time_list, error_group, label='disgroup')
        plt.plot(delay_time_list, error_disgroup_reduce, label='disgroup_reduce')
        plt.legend()
        plt.show()