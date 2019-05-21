import pytest

import seq2ftr.feature_calculators as fc

def test_mean():
    print(fc._max([12,9,10]))
    assert fc._mean([12,8,10])==10

