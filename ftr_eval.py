import pandas as pd
from woe import feature_process as fp
from woe import eval as evl

def calculate_ftr_iv(args):
    ftr,df,postive_sum,negative_sum,min_samples,alpha = args
    ftr_type_raw = str(df[ftr].dtype)
    if 'int' in ftr_type_raw or "float" in ftr_type_raw:
        fsummary = fp.proc_woe_continuous(df,ftr,postive_sum,negative_sum,min_sample=min_samples,alpha=alpha)
    else:
        fsummary = fp.proc_woe_discrete(df,ftr,postive_sum,negative_sum,min_sample=min_samples,alpha=alpha)
    return {ftr:fsummary.iv}

def iv_eval(df,ftr_cols,target='target',min_sample_rate = 0.05,min_samples = 100 ,alpha = 0.01, pool_size=1):
    positive_sum = df[target].sum()
    negative_sum = df.shape[0] - positive_sum
    min_samples = min(df.shape[0]*min_sample_rate,min_samples)
    if target!='target':
        df['target'] = df[target]
    if pool_size<=1:
        ivs = [calculate_ftr_iv((ftr,df,positive_sum,negative_sum,min_samples,alpha)) for ftr in ftr_cols]
    else:
        import multiprocessing
        p = multiprocessing.Pool(pool_size)
        ivs = p.map(calculate_ftr_iv,[(f,df,positive_sum,negative_sum,min_samples,alpha) for f in ftr_cols])
        p.close

    iv_dict= {}
    for i in ivs:
        iv_dict = {**i,**iv_dict}
    return iv_dict
