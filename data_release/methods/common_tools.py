import numpy as np

def add_noise(sensitivity, eps, num):
    noisy_arr = []
    if num > 1:
        for i in range(num):
            tmp = np.random.laplace(loc=0,scale=sensitivity/eps)
            noisy_arr.append(tmp)
                
        return noisy_arr
        
    else:
        return np.random.laplace(loc=0,scale=sensitivity/eps)
    
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