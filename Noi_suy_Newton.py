# test 1: chưa sắp xếp
# 1 2 3 4 7
# 17 17.5 76 210.5 1970

# test 2: đã sắp xếp, cách đều sau khi sắp xếp
# 5.75 5.8 5.85 5.9 5.95

# test 2: đã sắp xếp, không cách đều
# 5.75 5.8 5.85 5.9 5.95

# test 5: xắp xếp bị ngược, cách đều khi đảo lại
# 5.95 5.9 5.85 5.8 5.75


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def doc_input (ten_file):
    print("======================================================")
    print("Kieu du lieu dau vao: ")
    print("1. Ngang")
    print("2. Dọc")
    chon = int(input("chon kieu dau vao: "))
    if(chon == 1):
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

def kiem_tra_sap_xep(x):
    # tra ve 1 neu la sap xep tang dan
    # tra ve -1 neu la sap xep giam dan
    # tra ve 0 neu cac moc khong duoc sap xep
    if x[0] < x[1]:
        kieu_sap_xep = 1
    else:
        kieu_sap_xep = -1
    for i in range(x.shape[0] - 1):
        if x[i] < x[i + 1]:
            hien_tai = 1
        else:
            hien_tai = -1
        if abs(kieu_sap_xep - hien_tai) > 1e-7:
            return 0
    return kieu_sap_xep


def key_sort(z):
    return z[0]

def sap_xep_moc_noi_suy(x, y):
    z = list()  
    x0 = list()
    y0 = list()
    n = x.shape[0]
    for i in range(n):
        z.append(np.array([x[i], y[i]]))
    z.sort(key=key_sort)
    for i in range(n):
        x0.append(z[i][0])
        y0.append(z[i][1])
    return np.array(x0), np.array(y0)

def kiem_tra_cach_deu(x):
    # tra ve buoc nhay neu nhu cac moc cach deu
    # tra ve 0 neu du lieu khong cach deu
    denta = x[1] - x[0]
    for i in range(2, x.shape[0]):
        if abs(x[i] - x[i - 1] - denta) > 1e-7:
            return 0
    return 1

def kiem_tra_input (x, y):
    # tra ve 1 khi cac moc noi suy khong sap xep hoac khong cach deu
    # tra ve 2 khi cac moc noi suy la sap xep va cach deu
    # tra ve 0 khi cac moc noi suy trung nhau hoac kich thuoc cua x va y khac nhau

    # kiem tra kich thuoc du lieu
    if (x.shape[0] != y.shape[0]):
        print("kich thuoc khong hop le")
        return 0, x, y

    # kiem tra du lieu trung
    for i in x:
        if (np.where(x == i)[0].shape[0] > 1):
            print("du lieu cua x o cac vi tri ", np.where(x == i)[0], " trung nhau")
            return 0, x, y
    # input hop le
    print("input hop le")

    if(kiem_tra_sap_xep(x) == 1):
        if(kiem_tra_cach_deu(x)):
            return 2, x, y
            
    elif(kiem_tra_sap_xep(x) == 0):
        pass
        # x, y = sap_xep_moc_noi_suy(x, y)
        # if(kiem_tra_cach_deu(x)):
        #     return 2, x, y

    else:
        x = np.flip(x)
        y = np.flip(y)
        if(kiem_tra_cach_deu(x)):
            return 2, x, y

    return 1, x, y

def hoocne_product(x):
    # tich cua cac nghiem
    # Li luu he so da thuc sau moi lan nhan
    a = list()
    Li = [np.array([1])]
    a.append(np.array([1, 0]))
    for i in x:
        b = a[-1]
        c = list()
        c.append(1)
        for j in range(len(b) - 1):
            c.append(b[j + 1]- b[j] * i)
        c.append(0)
        a.append(np.array(c))
        Li.append(np.delete(a[-1], -1))
    return Li

def hoocne_quatient(a, x):
    # chia gia tri cua da thuc P(x) cho (x - x_0)
    # tra ve b và b_0 trong do:
    # b la he so cua da thuc sau khi chia
    # b_0 la phan du va la ket qua cua P(x_0)
    y = list()
    y.append(a[0])
    for i in range(len(a) - 1):
        y.append(y[i] * x + a[i + 1])
    b = np.array(y[:-1])
    b_0 = np.array(y[-1])
    return b, b_0

def noi_suy_moc_bat_ki(x, y):
    x = np.flip(x)
    y = np.flip(y)
    # tra ve he so cua da thuc noi suy theo moc bat ki theo bien x
    P = list()
    Z = list()
    Li = hoocne_product(x)
    for i in range(x.shape[0]):
        z = [y[i]]
        for j in range(i):
            z.append((z[j] - Z[i - 1][j]) / (x[i] - x[i - j - 1]))
        Z.append(np.array(z))
        Fi = Z[i][i]
        if i == 0:
            P.append(np.array(Fi * Li[i]))
        else:
            P.append(np.concatenate((np.array([0]), P[i - 1])) + Fi * Li[i])
    return P[-1]

def noi_suy_moc_cach_deu(x, y):
    # tra ve he so cua da thuc noi suy theo newton tien va theo bien t = (x - x0) / h
    P = list()
    Z = list()
    t = np.array(range(x.shape[0]))
    Li = hoocne_product(t)
    giai_thua = 1
    for i in range(x.shape[0]):
        if(i != 0):
            giai_thua *= i
        z = [y[i]]
        for j in range(i):
            z.append(z[j] - Z[i - 1][j])
        Z.append(np.array(z))
        Fi = Z[i][i]
        print(Fi)
        if i == 0:
            P.append(np.array((Fi * Li[i])/giai_thua))
        else:
            P.append(np.concatenate((np.array([0]), P[i - 1])) + (Fi * Li[i])/giai_thua)
    return P[-1]

def gia_tri_noi_suy_tai(P, x0):
    # tra ve gia tri cua y tai x0 neu la moc cach deu
    n = int((x.shape[0] - 1) / 2)
    t = (x0 - x[0])/h
    return hoocne_quatient(P, t)[1]

def ve_do_thi_da_thuc(P, x, y, k):
    a = np.ndarray.min(x)
    b = np.ndarray.max(x)
    h = (b - a) / 100
    x_i = [a]
    while(x_i[-1] < b):
        x_i.append(x_i[-1] + h)
    x_i = np.array(x_i, dtype=float)
    if k == 1:
        y_i = hoocne_quatient(P, x_i)[1]
    else:
        y_i = gia_tri_noi_suy_tai(P, x_i)
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

x, y = doc_input ("Test_case_NS_Newton.xlsx")
print("x = ",x)
print("y = ",y)
k, x, y = kiem_tra_input(x, y)
if(k == 1):
    print("su dung noi suy moc bat ki!")
    P = noi_suy_moc_bat_ki(x, y)
    print("===============================================")
    print("Ket thu qua sau khi thuc hien noi suy moc bat ki:")
    print("Da thuc noi suy theo x: ", bieu_dien_da_thuc(P))
    print("===============================================")
    ve_do_thi_da_thuc(P, x, y, k)
    x0 = float(input("Chon vi tri can tinh gia tri: "))
    if(x0 >= x[0] and x0 < x[-1]):
        print("gia tri can tinh nam trong khoang noi suy")
        print("gia tri cua y tai {} =".format(x0) , hoocne_quatient(P, x0)[1])
    else:
        print("gia tri can tinh nam ngoai khoang noi suy")

if(k == 2):
    print("su dung noi suy moc cach deu!")
    h = x[1] - x[0]
    P = noi_suy_moc_cach_deu(x, y)
    print("===============================================")
    print("Ket thu qua sau khi thuc hien noi suy moc cach deu:")
    print("Da thuc noi suy theo t: ", bieu_dien_da_thuc(P))
    print("===============================================")
    ve_do_thi_da_thuc(P, x, y, k)
    x0 = float(input("Chon vi tri can tinh gia tri: "))
    if(x0 >= x[0] and x0 < x[-1]):
        print("gia tri can tinh nam trong khoang noi suy")
        print("gia tri cua y tai {} =".format(x0) , gia_tri_noi_suy_tai(P, x0))
    else:
        print("gia tri can tinh nam ngoai khoang noi suy")