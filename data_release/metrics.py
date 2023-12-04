
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