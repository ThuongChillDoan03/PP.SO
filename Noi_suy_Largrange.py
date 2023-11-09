import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def doc_input (ten_file):
    print("======================================================")
    print("Kieu du lieu dau vao: ")
    print("1. Ngang")
    print("2. Dọc")
    chon = int(input("chon kieu dau vao: "))
    if(chon == 1):
        # doc file input.txt
        inp = pd.read_excel(ten_file)
        b = np.asarray(inp.astype(np.float64))
        # doc du lieu cua x va y
        x = b[0]
        y = b[1]
    else:
        inp = pd.read_excel(ten_file)
        b = np.asarray(inp.astype(np.float64))
        b = b.T
        x = b[0]
        y = b[1]
    return x, y

def kiem_tra_input (x, y):
    #tra ve 1 khi input hop le va 0 khi input khong hop le
    # kiem tra kich thuoc du lieu
    if (x.shape[0] != y.shape[0]):
        print("kich thuoc khong hop le")
        return 0
    
    # kiem tra du lieu trung
    for i in x:
        if (np.where(x == i)[0].shape[0] > 1):
            print("du lieu cua x o cac vi tri ", np.where(x == i)[0], " trung nhau")
            return 0
    # input hop le
    print("input hop le")
    return 1

def hoocne_quatient(a, x):
    # chia gia tri cua da thuc P(x) cho (x - x_0)
    # tra ve b và b_0 trong do:
    # b la he so cua da thuc sau khi chia
    # b_0 la phan du va la ket qua cua P(x)
    y = list()
    y.append(a[0])
    for i in range(len(a) - 1):
        y.append(y[i] * x + a[i + 1])
    b = np.array(y[:-1])
    b_0 = np.array(y[-1])
    return b, b_0

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

def D_i(x, i):
    # tinh tich cua x_i - x_j khi i != j, j = 0, n
    d = 1.0
    for j in range(x.shape[0]):
        if j != i:
            d *= x[i] - x[j]
    return d

def noi_suy_lagrange(x, y):
    n = x.shape[0]
    P = np.zeros(n)
    omega = hoocne_product(x)
    for i in range(n):
        Di = D_i(x, i)
        a = hoocne_quatient(omega, x[i])[0]
        Li = (1/Di)*a
        P += y[i]*Li
    return P

def ve_do_thi_da_thuc(x, y):
    a = np.ndarray.min(x)
    b = np.ndarray.max(x)
    h = (b - a) / 100
    x_i = [a]
    while(x_i[-1] < b - h):
        x_i.append(x_i[-1] + h)
    x_i = np.array(x_i, dtype=float)
    y_i = hoocne_quatient(P, x_i)[1]
    plt.plot(x_i, y_i)
    plt.plot(x, y, "o")
    plt.show()

def ve_do_thi_da_thuc(P, x, y):
    a = np.ndarray.min(x)
    b = np.ndarray.max(x)
    h = (b - a) / 100
    x_i = [a]
    while(x_i[-1] < b):
        x_i.append(x_i[-1] + h)
    x_i = np.array(x_i, dtype=float)
    y_i = hoocne_quatient(P, x_i)[1]
    plt.plot(x_i, y_i)
    plt.plot(x, y, "o")
    plt.xlabel("Truc X")
    plt.ylabel("Truc Y")
    plt.title("DO THI CUA DA THUC NOI SUY")
    plt.show()

def bieu_dien_da_thuc(P):
    da_thuc = ""
    for i in range(P.shape[0] - 1):
        da_thuc += "{}x^{} + ".format(round(P[i], 5), P.shape[0] - 1 - i)
    da_thuc += str(round(P[-1], 5))
    return da_thuc

x, y = doc_input ("Test_data_Largrange.xlsx")
if(kiem_tra_input(x, y)):
    P = noi_suy_lagrange(x, y)
    print("Da thuc noi suy theo x: ", bieu_dien_da_thuc(P))
    print("===============================================")
    ve_do_thi_da_thuc(P, x, y)

    ###_______________Nếu cần tính giá trị nào thì dùng thêm cái dưới này, if not thì cmt lại nhé!!!________###
    x0 = float(input("Chon vi tri can tinh gia tri: "))     
    if(x0 >= x[0] and x0 < x[-1]):
        print("gia tri can tinh nam trong khoang noi suy")
        print("gia tri cua y tai {} =".format(x0) , hoocne_quatient(P, x0)[1])
    else:
        print("gia tri can tinh nam ngoai khoang noi suy")
        