import numpy as np
from scipy.stats import entropy
from sklearn.metrics import mean_squared_error
from scipy.special import spence
# from boosting import boosting

import queue
import random

def boosting(Aq, lamda, mu, eta):
    if Aq <= lamda:
        aq = 1
    elif Aq >= lamda + mu:
        aq = -1
    else:
        aq=1-2 * (Aq - lamda) / mu
        
    return aq

def get_unique_random_number(small_numbers,medium_numbers,large_numbers,small_numbers_set,medium_numbers_set,large_numbers_set):
    while True:
        random_queue = random.choice([small_numbers, medium_numbers, large_numbers])
        if random_queue is small_numbers and not small_numbers.empty():
            number = small_numbers.get()
            small_numbers_set.remove(number)
            return number
        elif random_queue is medium_numbers and not medium_numbers.empty():
            number = medium_numbers.get()
            medium_numbers_set.remove(number)
            return number
        elif random_queue is large_numbers and not large_numbers.empty():
            number = large_numbers.get()
            large_numbers_set.remove(number)
            return number



def kldivergence(arra,arrb):
    div = np.sum(np.log(arra / arrb) * arra)
    return div


# Generate one sample
def synoposis_generator_pseu(n):
    p = [1/n] * n 
    sample = np.random.multinomial(n, p)
    synopsis = [x / sum(sample) for x in sample]
    return synopsis



# def random_budget_allocation(epsilon,mu,small_numbers,medium_numbers,large_numbers,small_numbers_set,medium_numbers_set,large_numbers_set):
#     a = 1
    
#     i = get_unique_random_number(small_numbers,medium_numbers,large_numbers,small_numbers_set,medium_numbers_set,large_numbers_set)

#     C=2/np.abs(a)/mu
    
#     m_square=spence((np.pi**2/6)-epsilon/C)**(-1)

#     eta=(np.e**((1-m_square**(2*i))/i/i/np.abs(a)) -1)/(np.e**((1-m_square**(2*i))/i/i/np.abs(a)) +1)
    
#     return eta

def framework(data, epsilon, tslot,lamda, mu):
    length_ = 50
    DEFAULT_DIST_LEN = length_
    tslot = np.floor(len(data) / length_)
    length = 6500 ## Define the synopsis pool size
    query_number = 2
    sampler_distribution_query = [[1/length] * length for _ in range(query_number)]
    queryset = []
    output_ds1=[]
    output_ks1=[]
    total_accum = np.zeros(DEFAULT_DIST_LEN)
    query = 1
    #print("%%%%%%")
    
    mae = 0
    c = 0
    for t in range(0,int(tslot)):

        ## Generate data
        #current_slot = np.random.normal(DEFAULT_DIST_LEN,sigma,DEFAULT_DIST_LEN)
        datas = np.zeros(length_, dtype=int)
        for ii in range(length_):
            datas[ii] = data[c]
            c += 1

        current_slot = datas
        current_slot[current_slot < 0] = 0
        total_accum += current_slot
        #current_slot /= np.sum(current_slot)


        ## Get budget
        #eta = random_budget_allocation(epsilon,mu,small_numbers,medium_numbers,large_numbers,small_numbers_set,medium_numbers_set,large_numbers_set)
        eta = epsilon*length_
        total_accum[total_accum < 0] = 0
        current_slot=np.array(current_slot)
        current_slot[current_slot < 0] = 0
        divs_acc = total_accum
        #divs_acc /= divs_acc.sum() #true answers pdf
        divs_cur = np.array(current_slot)
        #divs_cur /= divs_cur.sum()
        queryset.append(divs_acc)
        queryset.append(divs_cur)
        output = np.zeros(len(divs_acc))
        tmp = (1+2*eta)/(1-2*eta)
        if (1+2*eta)/(1-2*eta) < 0:
            tmp = 1
        alpha=1/2*np.log(tmp)

        synoposislist = [None] * length
        possible_outcomes = [i for i in range(length)]
        index_list=np.random.choice(possible_outcomes, 20, p=sampler_distribution_query[query]) ###### defined by domain size
        for i in index_list:

            structure=synoposis_generator_pseu(DEFAULT_DIST_LEN)
            output = [(output[m]+structure[m]) for m in range(len(structure))]
            while(structure in synoposislist):
                structure=synoposis_generator_pseu(DEFAULT_DIST_LEN)


            synoposislist[i]=structure
            l1_dist = np.linalg.norm(structure - divs_acc, ord=1)

            sampler_distribution_query[query][i]=boosting(l1_dist,lamda,mu,eta)

        uq1t=np.exp(alpha*np.sum(sampler_distribution_query[query]))
        for i in range(len(sampler_distribution_query[query])):
            sampler_distribution_query[query][i]=sampler_distribution_query[query][i]*uq1t
        sampler_distribution_query[query] = [x if x > 0 else 0.0001 for x in sampler_distribution_query[query]]
        sampler_distribution_query[query] /= np.sum(sampler_distribution_query[query])
        output /= np.sum(output)
        output = np.multiply(output, np.sum(current_slot))

        output_ds1.append(mean_squared_error(output, queryset[query]))
        output_ks1.append(entropy(queryset[query], output))

        mae += count_mae(divs_cur, output)

    return mae
    #return np.mean(output_ds1),np.mean(output_ks1)

def count_mae(ex, published_result):
    total_time = len(ex)
    published_time = len(published_result)
    #print(total_time, published_time)

    if total_time != published_time:
        print("error")
        return
    
    error_sum = 0

    for i in range(published_time):
        error_sum += abs(ex[i] - published_result[i])
    
    return error_sum / published_time

def main():
    #sensitivity = 2
    lamda=0.5
    mu=0.5
    tslot=1
    epsilon = 2
    # pritvate_result=framework(epsilon, tslot, DEFAULT_DIST_LEN,lamda, mu, small_numbers,medium_numbers,large_numbers,small_numbers_set,medium_numbers_set,large_numbers_set)

    ex = []
    filename = []
    
    count = 0
    filename = "./data_release/data/ILINet.csv"
    with open(filename, 'r', encoding='utf-8') as file_to_read:
        while True:

            lines = file_to_read.readline()
            count += 1
            if not lines:
                break
            elif count>= 3:
                tmp = lines.split(',')        
                ex.append([int(float(tmp[-1]))])


    # count = 0
    # filename = "./data_release/data/unemployment.csv"
    # with open(filename, 'r', encoding='utf-8') as file_to_read:
    #     while True:

    #         lines = file_to_read.readline()
    #         count += 1
    #         if not lines:
    #             break
    #         elif count>= 3:
    #             tmp = lines.split(',')        
    #             ex.append([int(tmp[-1])])

    length_ = len(ex)
    data = np.zeros(length_, dtype=int)
    for i in range(length_):
        data[i] = ex[i][0]

    epsilon_list = [0.1, 0.5, 1.0]
    
    pritvate_result = []
    round_ = 10
    for epsilon in epsilon_list:
        err = 0
        for r in range(round_):
            err += framework(data, epsilon, tslot, lamda, mu)
        err = err / round_

        pritvate_result.append(err)
        
    print(pritvate_result)
if __name__ == "__main__":
    main()