import hashlib
from functools import wraps
def set_property(*args):
    """
    The decorators for set properties for individual feature calculators
    :param args:
        name: the function's name for display
        stype: the supporting types for the feature calculating function
             0 for boolean, 1 for numericla, 2 for categorical
    :return:
    """
    def decorate_func(func):
        for i in range(0,len(args),2):
            setattr(func, args[i], args[i+1])
        return func
    return decorate_func

def listify_type(func):
    """
    Decorator for casting input to list
    :param func:
    :return:
    """
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
    """
    works similar to np.roll
    :param x:
    :param n:
    :return:
    """
    return x[n:]+x[:n]

def _sort(x:list):
    x_copy = x.copy()
    x_copy.sort()
    return x_copy
global x_sorted

def _appearance_count(x:list):
    """
    get frequency count
    :param x:
    :return:
    """
    freq = {k:0 for k in set(x)}
    for xi in x:
        freq[xi]+=1
    return freq
global x_freq_count

def _token_hash(x):
    """
    get input hash result
    :param key:
    :return:
    """
    if isinstance(x, str):
        x_md5 = hashlib.md5(x.encode("utf-8")).hexdigest()
        y = [int(v) for v in list(x) if v.isdigit()]
        y = sum(y)
        x_hash = hash(y)
    else:
        x_hash = hash(x)
    return x_hash


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

@set_property("name","variance","stypes",[1])
def _var(x:list):
    avg = _mean(x)
    return sum([(xi-avg)**2 for xi in x])/len(x)

@set_property("name","standard_deviation","stypes",[1])
def _std(x:list):
    return _var(x)**(0.5)

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

@set_property("name","last_location_of_max","stypes",[1])
def _last_location_of_max(x:list):
    xmax = _max(x)
    for i in range(1,len(x)+1):
        if x[-i] == xmax:
            return i

@set_property("name","fist_location_of_max","stypes",[1])
def _first_location_of_max(x:list):
    xmax = _max(x)
    for i in range(len(x)):
        if x[i] == xmax:
            return i

@set_property("name","last_location_of_min","stypes",[1])
def _last_location_of_min(x:list):
    xmin = _min(x)
    for i in range(1,len(x)+1):
        if x[-i] == xmin:
            return i

@set_property("name","fist_location_of_min","stypes",[1])
def _first_location_of_min(x:list):
    xmin = _min(x)
    for i in range(len(x)):
        if x[i] == xmin:
            return i

@set_property("name","ratio_value_number_to_seq_length","stypes",[1,2])
def _ratio_value_number_to_seq_length(x:list):
    return len(set(x))/_len(x)

@set_property("name","_number_peaks","stypes",[1])
@listify_type
def _number_peaks(x,n=1):
    counter = 0
    for i in range(n,len(x)-n):
        neighbors=[x[i-j] for j in range(1,n+1)] + [x[i+j] for j in range(1,n+1)]
        if x[i] > max(neighbors):
            counter+=1
    return counter

@set_property("name", "skewness", "stypes", [1])
@listify_type
def _skewness(x:list):
    avg = _mean(x)
    adjusted = [v - avg for v in x]
    count = len(x)
    adjusted2 = [pow(v,2) for v in adjusted]
    adjusted3 = [adjusted2[i] * adjusted[i] for i in range(len(adjusted))]
    m2 = sum(adjusted2)
    m3 = sum(adjusted3)

    if count<3:
        return None
    else:
        if m2 == 0:
            return 0
        else:
            result = (count * (count -1) ** 0.5 / (count - 2)) * (m3 / m2 ** 1.5)
            return round(result, 6)

@set_property("name","kurtosis", "stypes", [1])
@listify_type
def _kurtosis(x:list):
    avg = _mean(x)
    count = len(x)
    adjusted = [v - avg for v in x]
    adjusted2 = [pow(v,2) for v in adjusted]
    adjusted4 = [pow(v,2) for v in adjusted2]
    m2 = sum(adjusted2)
    m4 = sum(adjusted4)

    if count<4:
        return None
    else:
        adj = 3 * (count -1) ** 2 / ((count -2) * (count-3))
        numer = count * (count + 1) * (count - 1) * m4
        denom = (count - 2) * (count - 3) * m2 ** 2
        if denom == 0:
            return 0
        else:
            return round(numer/denom - adj, 6)

@set_property("name","categorical_max_freq_key_hash_code", "stypes", [2])
@listify_type
def _categorical_max_freq_key_hash_code(x:list):
    x_freq_count = _appearance_count(x)
    x_freq_count_sort = sorted(x_freq_count.items(), key=lambda d: d[1],reverse=True)
    x_max_freq_key = x_freq_count_sort[0][0]
    return _token_hash(x_max_freq_key)