
This project handles series data


Support Series data Feature Calculation.


Installation
==============

You need Python installed on your system to able to use seq2ftr.

This package contains many feature extraction methods.

Support different type (continues/class) features calculation.

>>> $ pip install seq2ftr

Install Requirements
 * numpy
 * pandas
 * sklearn


Feature Calculation
^^^^^^^^^^^^^^^^^^^^^^^^
 Support Function

 - mean
 - max
 - min
 - freq_of_max
 - freq_of_min
 - median
 - median_mean_distance
 - percentage_below_mean
 - var
 - std
 - uniqueCount
 - ...

Support Type
^^^^^^^^^^^^^^^^^
 - 0 - boolean
 - 1 - numericla
 - 2 - categorical


Example
^^^^^^^^^^^^^
To start , we load data to python

>>>
import pandas as pd
df = pd.DataFrame([[1,200,"1"],[1,500,"2"],[2,300,"2"],[2,600,"2"]],columns=['id','stock_price',"type"])
df = df.set_index("id")

>>>
from seq2ftr import SequenceTransformer
st_num = SequenceTransformer()
st_num.transformer(df['stock_price']）
# output all features



