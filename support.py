import math

def create_time(time):
    minute_score = math.trunc(time / 60000)
    second_score = math.trunc((time / 1000) % 60)
    millisecond_score = math.trunc((time % 1000) % 60)
    
    if second_score < 10 and millisecond_score < 10:
        score = f"{minute_score}: 0{second_score}: 0{millisecond_score}"
    elif second_score < 10:
        score = f"{minute_score}: 0{second_score}: {millisecond_score}"
    elif millisecond_score < 10:
        score = f"{minute_score}: {second_score}: 0{millisecond_score}"
    else:
        score = f"{minute_score}: {second_score}: {millisecond_score}"

    return score
    
def deconstruct_time(time):
    time_arr = time.split(':')
    rebuilt_time = ((int(time_arr[0])*60000)+(int(time_arr[1])*1000)+(int(time_arr[2])))

    return rebuilt_time