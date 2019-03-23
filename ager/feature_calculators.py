from functools import wraps
def set_property(*args):
    def decorate_func(func):
        for i in range(0,len(args),2):
            setattr(func, args[i], args[i+1])
        return func
    return decorate_func

def listify_type(func):
    @wraps(func)
    def listify(*args):
        x = args[0]
        if not isinstance(x,list):
            x = list(x)
        return func(x)
    return listify

##########################
## Supporting Funcitons ##
##########################
def _shift(x:list,n:int):
    return x[n:]+x[:n]

def _sort(x:list):
    x_copy = x.copy()
    x_copy.sort()
    return x_copy
global x_sorted

def _appearance_count(x:list):
    freq = {k:0 for k in set(x)}
    for xi in x:
        freq[xi]+=1
    return freq
global x_freq_count


#########################
## Feature Calculators ##
#########################
@set_property("name","mean","stypes",[0,1])
@listify_type
def _mean(x:list):
    return sum(x)/len(x)

@set_property("name","max","stypes",[0,1])
@listify_type
def _max(x:list):
    return max(x)

@set_property("name","freq_of_max","stypes",[1])
def _freq_of_max(x:list):
    max_x = _max(x)
    return len([xi for xi in x if xi >=max_x])

@set_property("name","min","stypes",[0,1])
@listify_type
def _min(x:list):
    return min(x)

@set_property("name","freq_of_min","stypes",[1])
def _freq_of_min(x:list):
    min_x = _min(x)
    return len([xi for xi in x if xi<=min_x])

@set_property("name",'median',"stypes",[1])
@listify_type
def _median(x:list):
    x_sorted = _sort(x)
    x_len = len(x_sorted)
    if x_len%2==1:
        return x_sorted[x_len//2]
    else:
        return x_sorted[x_len//2]*0.5 + x_sorted[x_len//2-1]*0.5

@set_property("name","median_mean_distance","stypes",[1])
def _median_mean_distance(x:list):
    return abs(_mean(x)-_median(x))/(_max(x)-_min(x))

@set_property("name","percentage_below_mean","stypes",[1])
def _percentage_below_mean(x:list):
    x_mean = _mean(x)
    return len([xi for xi in x if xi<x_mean])/_len(x)

@set_property("name","variance","stypes",[0,1])
def _var(x:list):
    avg = _mean(x)
    return sum([(xi-avg)**2 for xi in x])/len(x)

@set_property("name","uniqueCount","stypes",[0,1,2])
@listify_type
def _uniqueCount(x:list):
    return len(set(x))

@set_property("name","length","stypes",[0,1,2])
@listify_type
def _len(x:list):
    return len(x)

@set_property("name","duplicates_count","stypes",[0,1,2])
def _num_duplicates(x:list):
    return _len(x) - _uniqueCount(x)

@set_property("name","flucturate_rate","stypes",[0,2])
@listify_type
def _flucturate_rate(x:list,shift=1):
    x_shifted = _shift(x,shift)
    flucturate_vec = [xi1==xi2 for xi1,xi2 in zip(x[:-shift],x_shifted[:-shift])]
    return sum(flucturate_vec)/(len(x)-shift)

@set_property("name","percentage_of_most_reoccuring_value_to_all_values","stypes",[1,2])
@listify_type
def _percentage_of_most_reoccuring_value_to_all_values(x:list):
    x_freq_count = _appearance_count(x)
    return 1/len(x_freq_count)

@set_property("name","percentage_of_most_reoocuring_value_to_all_datapoints","stypes",[1,2])
@listify_type
def _percentage_of_most_reoocuring_value_to_all_datapoints(x:list):
    x_freq_count = _appearance_count(x)
    return max(x_freq_count.values()) / len(x)
