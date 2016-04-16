
import numpy as np

#非线性映射函数，到0~1的范围；及其导数，当deriv为True时
def nonlin(x,deriv=False):
    tanh=np.tanh(x)
    if(deriv==True):
        return (1-tanh**2)#此时，x是因变量，即从结果求导
    return tanh
