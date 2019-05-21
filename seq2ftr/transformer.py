__testdata__ = {
    "type":1,  # 0 for boolean, 1 for numericla, 2 for categorical
    "value":[1,2,3],
    "name":"sample_ftr",
}

from sklearn.base import TransformerMixin
import pandas as pd
import numpy as np
import seq2ftr.feature_calculators as fc
import logging

class SequenceTransformer(TransformerMixin):
    """
    Implemented Sklearn.base.TransformerMinMax for similar usage as sklearn.preprocessing.*transformers
    """
    def __init__(self,calculators:list = None,auto_adapt = True):
        """
        Constructtor
        :param calculators: You may specific a list of calculators' name for execution,
                            By default, all applicable functions are used.
        :param auto_adapt: the type (bool/numerical/categorical) of input X is
                            automatically detected by default, you may change to False accordingly,
                            warnings will be raised if the input x data type is not supported for calculators.
        """
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
        self.auto_adapt = auto_adapt
        if self.auto_adapt:
            fname2stypes = {fname:func.__dict__['stypes'] for fname,func in self.fns.items()}
            get_stype_fnames = lambda t: [fname for fname,stypes in fname2stypes.items() if t in stypes]
            self.type_fns = {k:get_stype_fnames(k) for k in range(3)}
        self.valid_fnames = list(self.fns.keys())

    def get_feature_names(self):
        """
        get feature names
        :return:
        """
        return list(self.valid_fnames)

    def fit(self,x:dict,y=None):
        """
        This is temporarally unimplemented until smoothnlp.learner is developed
        :param x:
        :param y:
        :return:
        """
        pass

    def transform(self,x):
        """
        A predefined data-format of x is transformed to feature

        sample input:

            __testdata__ = {
                "type":1,  # 0 for boolean, 1 for numericla, 2 for categorical
                "value":[1,2,3],
                "name":"sample_ftr",
            }

        :param x:
        :return:
        """
        if isinstance(x,pd.Series):
            x = self._transform_pd_series(x)
            ftr_transformed = [self.transform(d).values() for d in x.values]
            if x.name:
                col_names = [".".join([x.name,fname]) for fname in self.get_feature_names()]
            else:
                col_names = self.get_feature_names()
            df_ftr = pd.DataFrame(ftr_transformed,columns=col_names)
            df_ftr.index = x.index
            return df_ftr
        if not isinstance(x,dict):
            try:
                x = self._auto_type_transform(x)
            except IndexError:
                return None
        if "type" not in x.keys():
            x = self._auto_type_transform(x)

        if len(x['value'])<1:
            self.logger.fatal("sequence input is empty")
            return None

        ftrs = {}
        if not self.auto_adapt:
            executing_fns = self.fns.keys()
        else:
            executing_fns = self.type_fns[x['type']]
        for fname in executing_fns:
            if self._check_stype(fname,x):
                ftrs[fname] = (self._transform_fn(fname,x['value']))
        self.valid_fnames = list(ftrs.keys())
        if "name" in x.keys():
            ftrs = {".".join([x['name'],key]):value for key,value in ftrs.items()}
        return ftrs

    def _check_stype(self,fname,x):
        """
        check support types of a specific function, if unsupported raise warning
        :param fname:
        :param x:
        :return:
        """
        fn_stypes = getattr(self.fns[fname],"stypes")
        if x['type'] not in fn_stypes:
            self.logger.critical("There is a mismatch between input X and calculator({}) supporting types".format(fname))
            return False
        return True

    def _transform_fn(self,fname,v):
        f = self.fns[fname]
        try:
            return f(v)
        except ZeroDivisionError:
            return 0

    def _transform_numpy_array(self):
        ## import numpy as np
        ## TODO
        ## Numpy Transformation may not be supported
        pass

    def _transform_pd_series(self, series):
        ## TODO
        series = series.groupby(series.index).agg(lambda x: list(x))
        return series

    def _auto_type_transform(self,x):
        """
        if x is input merely as a list of values or a dict of input format without type indicator,
        x's type is automatically detected
        :param x:
        :return:
        """
        if isinstance(x,list):
            if len(x)<1:
                error_msg = "Input X has invalid length: {}".format(len(x))
                self.logger.critical(error_msg)
                raise IndexError(error_msg)
            x = list(x) if not isinstance(x,list) else x
            sample_x = x[0]
            if isinstance(sample_x,bool):
                xtype = 0
            elif isinstance(sample_x,(int,float,np.int64,np.int32,np.float32,np.float64)):
                xtype = 1
            else:
                xtype = 2
            return {"type":xtype,"value":x}
        elif isinstance(x,dict):
            if "name" not in x:
                self.logger.warning("A sequence's name is highly recommended for multiple sequence modeling")
            transformed_result = self._auto_type_transform(x['value'])
            transformed_result['name'] = x['name']
            return transformed_result


class MultiSequenceTransformer(TransformerMixin):
    def __init__(self,seqname2transformers = {}):
        self.seqname2transformers = seqname2transformers
        self.logger = logging.getLogger()


    def fit(self,X:dict,y = None):
        if isinstance(X,dict):
            x_keys = X.keys()
            for x_key in x_keys:
                if x_key not in self.seqname2transformers:
                    self.seqname2transformers[x_key] = SequenceTransformer()
                    self.seqname2transformers[x_key].fit(X[x_key])
        if isinstance(X,list):
            for xi in X:
                self.fit(xi)

    def transform(self,X):
        if isinstance(X,dict):
            x_res = {}
            for x_key,x_item in X.items():
                if x_key not in self.seqname2transformers:
                    self.logger.critical("sequence with name '{}' is not fitted, therefore may not be transformer.".format(x_key))
                    continue
                x_res = {**x_res,**self.seqname2transformers[x_key].transform(x_item)}
            return x_res
        if isinstance(X,list):
            return [self.transform(xi) for xi in X]


# _multi_test_data = {'sourceToken': {'name': 'sourceToken',
#   'value': ['支出', '申请', '支付', '发', '消费', '剩余', 'unknown', '剩余', '借']},
#  'moneyNormalizedAmount': {'name': 'moneyNormalizedAmount',
#   'value': [2350.6, 5000, 1400, 2000, 148, 475.25, 400, 1475.23, 300]}}
#
# mst = MultiSequenceTransformer()
# mst.fit(_multi_test_data)
# print(mst.transform(_multi_test_data))