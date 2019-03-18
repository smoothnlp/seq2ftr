__testdata__ = {
    "type":1,  # 0 for boolean, 1 for numericla, 2 for categorical
    "value":[1,2,3]
}

from sklearn.base import TransformerMixin
import featre_calculators as fc
import logging

class SequenceTransformer(TransformerMixin):
    def __init__(self,calculators:list = None):
        all_fns = {getattr(fc,fn).__dict__['name']:getattr(fc,fn) for fn in dir(fc) if callable(getattr(fc,fn)) and 'name' in getattr(fc,fn).__dict__}
        self.logger = logging.getLogger()
        if calculators is None:
            self.fns = all_fns
        else:
            self.fns = {}
            for c in calculators:
                if c not in all_fns:
                    self.logger.warning("calculator {} is not supported in the latest version of feature calculators".format(c))
                else:
                    self.fns[c] = all_fns[c]
        self.valid_fnames = list(self.fns.keys())

    def get_feature_names(self):
        return list(self.valid_fnames)

    def fit(self,x:dict,y=None):
        pass

    def transform(self,x):
        if not isinstance(x,dict):
            x = self._auto_type_transform(x)
        ftrs = {}
        for fname in self.fns:
            if self._check_stype(fname,x):
                ftrs[fname] = (self._transform_fn(fname,x['value']))
        self.valid_fnames = list(ftrs.keys())
        return ftrs

    def _check_stype(self,fname,x):
        fn_stypes = getattr(self.fns[fname],"stypes")
        if x['type'] not in fn_stypes:
            self.logger.critical("There is a mismatch between input X and calculator({}) supporting types".format(fname))
            return False
        return True

    def _transform_fn(self,fname,v):
        f = self.fns[fname]
        return f(v)

    def _transform_numpy_array(self):
        import numpy as np
        ## TODO
        pass

    def _transform_pd_series(self):
        import pandas as pd
        ## TODO
        pass

    def _auto_type_transform(self,x):
        if len(x)<1:
            error_msg = "Input X has invalid length: {}".format(len(x))
            self.logger.critical(error_msg)
            raise Exception(error_msg)
        x = list(x) if not isinstance(x,list) else x
        sample_x = x[0]
        if isinstance(sample_x,bool):
            xtype = 0
        elif isinstance(sample_x,int) or isinstance(sample_x,float):
            xtype = 1
        else:
            xtype = 2
        return {"type":xtype,"value":x}




