def set_property(key, value):
    def decorate_func(func):
        setattr(func, key, value)
        # if key=="name":
        #     setattr(func,"__doc__","The calculator's name is {}".format(value))
        return func
    return decorate_func

def support_type(nums):
    def decorate_func(func):
        setattr(func, "stypes", nums)
        return func
    return decorate_func


@set_property("name","mean")
@support_type([0,1])
def _mean(x:list):
    if isinstance(x,list):
        x = list(x)
    return sum(x)/len(x)

@set_property("name","max")
@support_type([0,1])
def _max(x:list):
    if isinstance(x,list):
        x = list(x)
    return max(x)

@set_property("name","min")
@support_type([0,1])
def _min(x:list):
    if isinstance(x,list):
        x = list(x)
    return min(x)

@set_property("name","variance")
@support_type([0,1])
def _var(x:list):
    avg = _mean(x)
    return sum([(xi-avg)**2 for xi in x])/len(x)


@set_property("name","uniqueCount")
@support_type([0,1,2])
def _uniqueCount(x:list):
    return len(set(x))
