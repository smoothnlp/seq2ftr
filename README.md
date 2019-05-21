# seq2ftr
> * Sequence data to features 
> * 一个**高性能**、**可扩展**、**数据科学友好**的序列数据特征工具

## Install
* 通过 pip 安装
```shell
pip install seq2ftr 
```

* 通过源码安装
```shell
git clone https://github.com/smoothnlp/seq2ftr.git
cd seq2ftr 
python setup.py install 
```


## About (关于seq2ftr项目)
* 高性能、python工程化完成度：
    - *第三方依赖*：
相比较于当前sequence处理最火的开源项目*tsfresh*, seq2ftr 项目中对数据处理和计算时减少了不必要的第三方包依赖，在特征计算逻辑中：feature_calculator.py 中不依赖任何外部开源包，全部原生实现
    - *数据结构的统一*： 
    原始数据在输入层面尽支持继承python原生iterable的数据结构,在进入特征计算流程之前, 全部被归一化成 list 数据结构. (后期为了节省内存空间， 可考虑重构成tuple数据结构)
* 可扩展
    - seq2ftr中最重要的计算逻辑feature_calculators.py, 在新增特征计算逻辑中， 仅需考虑输入为list数据结构的input，对外部项目架构不需要有过多的认知即可。在开发时请注意，将使用`decorator`在新增的特征计算逻辑添加`name` 这个attribute, 下面是一个例子：
    ```python3
    @set_property("name","mean","stypes",[0,1])
    @listify_type
    def _mean(x:list):
        return sum(x)/len(x)
    ```
* 数据科学友好性
    - 继承sklearn.base.TransformerMinMax: 
    seq2ftr 中的 transformer 使用和sklearn保持了完全一致，方便了数据科学家的快速建模与评估，与后期类似DataFrameMapper这样的数据处理工具（待测试），下面是例子”
    ```python3
    import pandas as pd
    df = pd.DataFrame([[1,200,"1"],[1,500,"2"],[2,300,"2"],[2,600,"2"]],columns=['id','stock_price',"type"])
    df = df.set_index("id")
    
    from seq2ftr import SequenceTransformer
    st_num = SequenceTransformer()
    st_num.transform(df['stock_price'])
    ```


    
##  [QuickDemo](https://github.com/zhangruinan/Ager/blob/master/QuickDemo.ipynb)


