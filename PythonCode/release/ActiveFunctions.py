
import numpy as np

#非线性映射函数，到0~1的范围；及其导数，当deriv为True时
def nonlin(x,deriv=False):
    y=np.tanh(x)
    if deriv:
        return (1-y**2)
    return y
