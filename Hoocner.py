import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Hàm hoocner chia để tính giá trị đa thức tại x = c
def hoocnerDivide(a, c):
    Q = []
    Q.append(a[0])
    for i in range(1, len(a)):
        Q.append(Q[i - 1] * c + a[i])
    return Q

# Hàm đạo hàm bậc k của đa thức tại x = c
def DerivativeDegree_K(a, c, k):
    if k > len(a) - 1:
        value = 0
    else:
        value = 1
        Q = hoocnerDivide(a, c)
        for i in range(k, 0, -1):
            Q.remove(Q[len(Q) - 1])
            Q = hoocnerDivide(Q, c).copy()
            value *= i
        value *= Q.pop()
    return value


###______________Test_case_Giá trị của P_n(c)________________###
# a = [1, -10, 35, -50, 24]
# c = 5

# p_n_c = hoocnerDivide(a, c).pop()
# print(p_n_c)

###______________Test_case_Giá trị tại đạo hàm cấp k của P_n(k)(c)_____###

# a = [1, -10, 35, -50, 24]
# # Nhập giá trị c
# c = 5
# # Nhập giá trị k (bậc đạo hàm)
# k = 3

# P_n_k_c = DerivativeDegree_K(a, c, k)
# print(P_n_k_c)

###____________Xác định đa thức thương P_n(x)/(x-c) ____________###

a = [1, -10, 35, -50, 24]
# Nhập giá trị c
c = 5
Q = hoocnerDivide(a, c)
Q.remove(Q[len(Q) - 1])
for i in range(len(Q)):
    print("{0}x^{1}".format(Q[i], len(Q) - 1 - i))

