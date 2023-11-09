import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def hoocne_quatient(a, x):
    # chia gia tri cua da thuc P(x) cho (x - x_0)
    # tra ve b và b_0 trong do:
    # b la he so cua da thuc sau khi chia
    # b_0 la phan du va la ket qua cua P(x_0)
    y = []
    y.append(a[0])
    for i in range(len(a) - 1):
        y.append(y[i] * x + a[i + 1])
    b = np.array(y[:-1])
    b_0 = np.array(y[-1])
    return b, b_0

def hoocne_derivative(a, k, x):
    # tinh dao ham bac k cua da thuc P(x)
    # tra ve gia tri cua dao ham
    y = list()
    y.append(a)
    for i in range(k):
        b, b_0 = hoocne_quatient(y[i], x)
        y.append(b)
    b, b_0 = hoocne_quatient(y[-1], x)
    return b_0 * k

def hoocne_product(x):
    #tich cua cac nghiem
    # a la he so sau khi nhan tat ca ca nghiem
    a = list()
    a.append(np.array([1, 0]))
    for i in x:
        b = a[-1]
        c = list()
        c.append(1)
        for j in range(len(b) - 1):
            c.append(b[j + 1]- b[j] * i)
        c.append(0)
        a.append(np.array(c))
    return np.delete(a[-1], -1)

# doc file excel
ind = pd.read_excel("Data_XXPP_dathuc.xlsx")
b = np.asarray(ind.astype(np.float64))
a = b[0]
print(a)


while(True):
    print("1. Hoocne quatient")
    print("2. quatient polynomial")
    print("3. Hoocne derivative degree k")
    print("4. Hoocne product")

    choose = int(input("Chon chuc nang ban muon su dung: "))

    if (choose == 1):
        x = float(input("Nhap gia tri cua x0: "))
        b, b_0 = hoocne_quatient(a, x)
        print("Hệ số của đa thức khi chia: ", b)
        print("P({}) = {}".format(x, b_0))

    elif (choose == 2):
        x =float(input("Nhap gia tri cua x0: "))
        b, b_0 = hoocne_quatient(a, x)
        print("P(x)/(x - {}) = ".format(x), end = "")
        for i in range(b.shape[0]):
            print("{}x^{} + ".format(b[i], len(b) - 1 - i), end = "")
        print("{}/(x - {})".format(b_0, x))

    elif (choose == 3):
        x = float(input("Nhap gia tri cua x0: "))
        k = int(input("Nhap so bac cua dao ham: "))
        print("giá đạo hàm cấp {} của P tại x = {} là: {}".format(k, x, hoocne_derivative(a, k, x))) 

    elif (choose == 4):
        b = hoocne_product(a)
        for i in range(b.shape[0] - 1):
            print("{}x^{} + ".format(b[i], b.shape[0] - 2 - i), end = "")
        print(b[-1])

    else:
        break