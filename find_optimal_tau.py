import numpy as np
import matplotlib.pyplot as plt

# verify the optimization distribution
# def find_tau(data, start_, end_, length, epsilon, delta_):
    
#     c = 0
#     err_ = np.zeros(end_ - start_ + 1, dtype=float)
#     for tau_ in range(start_, end_ + 1):
#         count_ = 0
#         # count number of data larger than \tau
#         for i in range(1, len(data)):
#             if (data[i] - data[i-1]) > tau_:
#                 count_ += 1
#         print(count_)

#         err_[c] = np.sqrt(2) * length * delta_ * count_ / epsilon + (length - count_) * tau_
#         c += 1

#     x_arry = np.zeros(end_ - start_ + 1, dtype=int)
#     c = 0
#     for j in range(start_, end_ + 1):
#         x_arry[c] = j
#         c += 1
    
#     plt.plot(x_arry, err_)
#     plt.show()

# serach the optimal threshold tau from the strat_ 
# def find_init_tau(data, start_, end_, length, epsilon, delta_):
    
#     err_pre = 0
#     flag_num = 0
#     for tau_ in range(start_, end_ + 1):
#         count_ = 0
#         # count number of data larger than \tau
#         for i in range(1, len(data)):
#             if (data[i] - data[i-1]) > tau_:
#                 count_ += 1

#         err_ = np.sqrt(2) * length * delta_ * count_ / epsilon + (length - count_) * tau_

#         if err_ >= err_pre and tau_ > start_:
#             flag_num += 1
#             if flag_num > end_ / 5:
#                break
#         else:
#             flag_num = 0
#             optimal_tau_ = tau_
        
#         err_pre = err_
#         #print(err_ / length)
        
#     return optimal_tau_, count_

def find_init_tau(data, length, epsilon, delta_):
    
    dis = np.zeros(length - 1, dtype=float)
    # count number of data larger than \tau
    for i in range(1, length):
        dis[i - 1] = abs(data[i] - data[i - 1])

    dis.sort()
    
    err_pre = np.sqrt(2) * length * delta_ * (length - 2) / epsilon + dis[0]
    for i in range(1, length - 1):

        err_ = np.sqrt(2) * length * delta_ * (length - i - 2) / epsilon + (i + 1) * dis[i]
        #print(err_)

        if err_ > err_pre:
            optimal_tau_ = dis[i - 1]
            break
        elif i == length - 2:
            optimal_tau_ = dis[i]
            break
        else:
            err_pre = err_
        #print(err_ / length)
        
    return optimal_tau_, length - i - 2

def find_tau(data, start_, end_, length, epsilon, delta_):
    
    err_ = np.zeros(length - 1, dtype=float)
    dis = np.zeros(length - 1, dtype=float)
    # count number of data larger than \tau
    for i in range(1, length):
        dis[i - 1] = abs(data[i] - data[i - 1])

    dis.sort()
    
    err_[0] = np.sqrt(2) * length * delta_ * (length - 2) / epsilon + dis[0]
    for i in range(1, length - 1):

        err_[i] = np.sqrt(2) * length * delta_ * (length - i - 2) / epsilon + (i + 1) * dis[i]
        #print(err_)
    
    plt.plot(dis, err_)
    plt.show()

# search the optimal threshold tau from the previous optimal threshold tau
def update_tau(data, start_, end_, length, epsilon, delta_, current_tau):

    count_current = 0
    count_next = 0
    for i in range(1, len(data)):
        if (data[i] - data[i-1]) > current_tau:
            count_current += 1

        if (data[i] - data[i-1]) > current_tau + 1:
            count_next += 1

    current_err = np.sqrt(2) * length * delta_ * count_current / epsilon + (length - count_current) * current_tau
    next_err = np.sqrt(2) * length * delta_ * count_next / epsilon + (length - count_next) * (current_tau + 1)
    #print(current_err, next_err)

         
    if next_err < current_err:
        optimal_tau_, count_ = find_init_tau(data, current_tau + 1, end_, length, epsilon, delta_)
    else:
        optimal_tau_, count_ = find_init_tau(data, start_, current_tau, length, epsilon, delta_)

    return optimal_tau_, count_

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
    w = 120

    data = np.zeros(w, dtype=int)
    for i in range(w):
        data[i] = ex[i][0]

    print(max(data))
    
    
    epsilon = 1
    delta_ = max(data)
    optimal_tau_, count_= find_init_tau(data, w, epsilon, delta_)
    #find_tau(data, 1, max(data), w, epsilon, delta_)
    #optimal_tau_, count_= update_tau(data, min(data), max(data), w, epsilon, delta_, 200)
    print(optimal_tau_, count_)
    