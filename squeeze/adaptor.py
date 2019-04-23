from sklearn.base import TransformerMixin

_test_data_ = [{'charStart': '0',
  're': '0.0',
  'phrase_score': '0.9810855061190058',
  'le': '0.0',
  'charEnd': '2',
  'tokenIndex': '0',
  'textRankScore': '0.57032394',
  'pmi': '11.326906499272114',
  'token': '今天'},
 {'charStart': '2',
  're': '0.6365141682948128',
  'phrase_score': '30.39080850692747',
  'le': '0.6365141682948128',
  'charEnd': '4',
  'tokenIndex': '1',
  'textRankScore': '0.9089106',
  'pmi': '11.961213179809127',
  'token': '天气'}]

import collections
import logging

def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def _auto_xval_type_convert(xval):
    try:
        return int(xval)
    except ValueError:
        try:
            return float(xval)
        except ValueError:
            return xval


class adapator():
    def __init__(self,index_ftrs:list, val_ftrs:list=None, sortByIndexs = False):
        self.index_ftrs = index_ftrs
        self.val_ftrs = val_ftrs
        self.logger = logging.getLogger()

    def convert2seqs(self,x:list):
        valid_val_ftrs = self.figure_val_ftrs(x[0])
        seqs = {k:{"name":k,"value":[]} for k in valid_val_ftrs}
        for x_i in x:
            if not isinstance(x_i,dict):
                raise TypeError("each element in x should be dict, instead get: {}".format(str(type(x_i))))
            for fname in valid_val_ftrs:
                if fname not in x_i:
                    # self.logger.warning("{} is not in every element of the input x.".format(fname))
                    continue
                if x_i[fname] is not None:
                    seqs[fname]['value'].append(_auto_xval_type_convert(x_i[fname]))
                else:
                    seqs[fname]['value'].append(None)
        return seqs

    def figure_val_ftrs(self,x_i:dict):
        if self.val_ftrs:
            return self.val_ftrs
        index_leftover_ftrs = set(x_i.keys()) - set(self.index_ftrs)
        return list(index_leftover_ftrs)


smoothnlp_document_token_adaptor = adapator(index_ftrs=['charStart',"charEnd","tokenIndex"],
                                     val_ftrs=['re','le',"pmi",'phrase_score',"textRankScore","token"])

smoothnlp_money_ner_adaptor = adapator(index_ftrs=['charStart',"charEnd"],
                                     val_ftrs=['sourceToken',"moneyNormalizedAmount"])

