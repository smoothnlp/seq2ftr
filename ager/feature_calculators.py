from functools import wraps
def set_property(*args):
    def decorate_func(func):
        for i in range(0,len(args),2):
            setattr(func, args[i], args[i+1])
        return func
    return decorate_func

def listify_type(x):
    @wraps(x)
    def listify(x):
        if not isinstance(x,list):
            x = list(x)
        return x
    return listify

@set_property("name","mean","stypes",[0,1])
@listify_type
def _mean(x:list):
    return sum(x)/len(x)

@set_property("name","max","stypes",[0,1])
@listify_type
def _max(x:list):
    return max(x)

@set_property("name","min","stypes",[0,1])
@listify_type
def _min(x:list):
    return min(x)

@set_property("name","variance","stypes",[0,1])
@listify_type
def _var(x:list):
    avg = _mean(x)
    return sum([(xi-avg)**2 for xi in x])/len(x)


@set_property("name","uniqueCount","stypes",[0,1,2])
@listify_type
def _uniqueCount(x:list):
    return len(set(x))
