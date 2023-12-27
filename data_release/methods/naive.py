import common_tools

def naive_event(ex, sensitivity_, eps):
    total_time = len(ex)
    dim = len(ex[0])

    published_result = []

    for i in range(total_time):
        noise_result = ex[i][0] + common_tools.add_noise(sensitivity_, eps, dim)
        published_result.append(noise_result)

    return published_result


def run_naive_event(ex, sensitivity_, epsilon_list, round_):
    error_ = []
    for eps in epsilon_list:
        err_round = 0
        for j in range(round_):
            published_result = naive_event(ex, sensitivity_, eps)
            err_round += common_tools.count_mae(ex, published_result)

        error_.append(err_round / round_)

    return error_