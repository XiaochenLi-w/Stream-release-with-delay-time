import numpy as np
import matplotlib.pyplot as plt

from other_competitor.adapub import Adapub
import methods.common_tools

def est_sens_opt(ex_, domain_low, domain_high, epsilon_list, round_):
    
    error_adapub = []
    for para_eps in epsilon_list:
        error_ = 0
        mech = Adapub(para_eps, len(ex_), 1)
    
        for r in range(round_):
            op, publish_num = mech.run(ex_, domain_high)
            error_ += methods.common_tools.count_mae(ex_, op)
        
        error_adapub.append(error_/round_)
    
        
    # error = []
    # error.append(error_naive)
    # error.append(error_pegasus_delay)
    # error.append(error_pegasus_nodelay)
    # error.append(error_continred)
    # error.append(error_discontinpp)
    # error.append(error_discontinred)
    # error.append(error_order)
    # error.append(error_order_advance)

    # np.savetxt('result.txt', error)

    # print('naive:', error_naive)
    # print('pegasus:', error_pegasus_nodelay)
    # print('PeGaSus_delaypp:', error_pegasus_delay)
    # print('contin_noisered_close:', error_continred)
    # print('discontin_pp:', error_discontinpp)
    # print('discontin_reduce:', error_discontinred)
    # print('Order_based:', error_order)
    # print('order_adv:', error_order_advance)
    # print(error_naive[0], ',', error_pegasus_delay[0], ',', error_discontinpp[0], ',', error_order[0], ',', error_order_advance[0])
    # print(error_discontinred[0], ',', error_order[0], ',', error_order_advance[0])
    print(error_adapub)

    # plt.plot(epsilon_list, error_naive, label='naive')
    # plt.plot(epsilon_list, error_order, label='order')
    # plt.plot(epsilon_list, error_continred, label='continred')
    # plt.plot(epsilon_list, error_pegasus_delay, label='pegasus_delay')
    # plt.plot(epsilon_list, error_pegasus_nodelay, label='pegasus_nodelay')
    # plt.plot(epsilon_list, error_discontinpp, label='discontinpp')
    # plt.plot(epsilon_list, error_discontinred, label='discontinred')
    # plt.plot(epsilon_list, error_order_advance, label='order_advance')
    # plt.legend()
    # plt.show()


if __name__ == "__main__":

    ex = []
    filename = []
    
    # count = 0
    # ex1 = []
    # #filename1 = "./data/COVID19 DEATH.csv"
    # filename1 = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/COVID19 DEATH.csv"
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
    # ex5 = []
    # #filename5 = "./data/National_Custom_Data.csv"
    # filename5 = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/National_Custom_Data.csv"
    # with open(filename5, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 0:
    #             tmp = lines.split(',')
                
    #             ex5.append([int(float(tmp[-2]))])
    # ex.append(ex5)
    # filename.append(filename5)
    
    # count = 0
    # ex7 = []
    # #filename7 = "./data/unemployment.csv"
    # filename7 = "D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/unemployment.csv"
    # with open(filename7, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 3:
    #             tmp = lines.split(',')        
    #             ex7.append([int(tmp[-1])])

    # ex.append(ex7)
    # filename.append(filename7)

    # count = 0
    # ex8 = []
    # filename8 = "./data/footmart.csv"
    # with open(filename8, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         else:
    #             tmp = lines.split(',')        
    #             ex8.append([int(tmp[-1])])

    # ex.append(ex8)
    # filename.append(filename8)

    # count = 0
    # ex9 = []
    # filename9 = "./data/OnlineRetail.csv"
    # with open(filename9, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         else:
    #             tmp = lines.split(',')        
    #             ex9.append([int(tmp[-1])])

    # ex.append(ex9)
    # filename.append(filename9)

    count = 0
    ex9 = []
    filename9 = "./data/ILINet.csv"
    with open(filename9, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            else:
                tmp = lines.split(',')        
                ex9.append([int(tmp[-1])])

    ex.append(ex9)
    filename.append(filename9)

    for k in range(len(ex)):
        print('#It is the results of', filename[k])

        length_ = len(ex[k])
        data = np.zeros(length_, dtype=int)
        for i in range(length_):
            data[i] = ex[k][i][0]

        round_ = 20
        #epsilon_list = [0.00001, 0.00002, 0.00003, 0.00004, 0.00005]
        epsilon_list = [0.1, 0.5, 1.0]
        #epsilon_list = [0.5]
        print('data domain:', min(data), max(data))
        #sensitivity_ = 1

        est_sens_opt(ex[k], min(data), max(data), epsilon_list, round_)
    