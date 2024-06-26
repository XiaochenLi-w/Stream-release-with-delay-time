import numpy as np

def laplace(beta, data):
    output = data + np.random.laplace(0, beta, len(data))
    return output


# noisy max
def nm(q_ans, eps, sensitivity=1, monotonic=True):
    coeff = eps / sensitivity if monotonic else eps / 2 / sensitivity
    noisy_ans = laplace(1 / coeff, q_ans)

    return np.argmax(noisy_ans)


def quality_func(data, sensitivity_low, sensitivity_upper, interval_, eps):
    m = len(data)
    
    num = (sensitivity_upper - sensitivity_low + 1) // interval_
    possible_sens = np.zeros(num, dtype=float)
    c = 1
    for i in range(num):
            possible_sens[i] = sensitivity_low + c * interval_
            c += 1

    np.sort(data)

    sum_value = np.zeros(m, dtype = float)
    sum_value[0] = np.sum(data)
    for i in range(1, m):
        sum_value[i] = sum_value[i-1] - data[i-1]
    
    q_ans = np.zeros(num, dtype=float)

    for i in range(num):
        idx = np.where(data > possible_sens[i])
        
        if len(idx[0]) == 0:
            benfit_ = m * np.sqrt(2) * (sensitivity_upper - possible_sens[i]) / eps
            lost_ = 0
        else:
            benfit_ = m * np.sqrt(2) * (sensitivity_upper - possible_sens[i]) / eps
            lost_ = (sum_value[idx[0][0]] - (m - idx[0][0]) * possible_sens[i])

        

        q_ans[i] = (benfit_ - lost_) / (m * sensitivity_upper)
    
        #print(var_ / m, std_ / m)
    sample_result = nm(q_ans, eps)
    #print(q_ans)
    
    #sample_result = np.argmax(q_ans)
    print('new_sens', possible_sens[sample_result])
    
    return possible_sens[sample_result]

if __name__ == "__main__":

    ex = []
    filename = []

    # count = 0
    # ex1 = []
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
    # ex7 = []
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


    count = 0
    ex5 = []
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

    epsilon = 0.5
    sensitivity_low = min(data)
    sensitivity_upper = max(data)
    print(sensitivity_low, sensitivity_upper)
    interval_ = 20

    new_sens = quality_func(data, sensitivity_low, sensitivity_upper, interval_, epsilon)