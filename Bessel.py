import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# THUẬT TOÁN DÀNH CHO SỐ MỐC CHẴN, CÁCH ĐỀU


def doc_input (ten_file):
    print("======================================================")
    print("Kieu du lieu dau vao: ")
    print("1. Ngang")
    print("2. Doc")
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
    # thuc hien sap xep moc noi suy neu cac moc chua duoc sap xep
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
    return denta

def kiem_tra_chan_le(x):
    # tra ve 0 neu so moc noi suy la chan
    # tra ve 1 neu so moc noi suy la le
    n = x.shape[0]
    if(n % 2 == 0):
        return 0
    else:
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

def bessel(x, y):
    # tra ve he so cua da thuc sau khi thuc hien stirling theo bien t = (x - x0)/h
    n = int((x.shape[0] - 1) / 2)
    print("n =", n)
    giai_thua = 1
    t = list()
    P = list()
    P1 = [np.array([(y[n] + y[n + 1])]) / 2]
    P2 = [np.array([y[n + 1] - y[n]])]
    print(P2[-1])
    Z1 = [y[n], y[n + 1] - y[n]]
    Z2 = [y[n + 1], y[n + 1] - y[n]]
    
    # luu he so cua da thuc khi nhan lan luot Li cho (t^2 - i^2)
    for i in range(1, n + 1):
        t.append(((2*i - 1) / 2)**2)
    Li = hoocne_product(t)
    print("Li = ", Li)
    
    # vao vong lap
    for i in range(1, n + 1):
        print("=======================================")
        print("vong lap thu:", i)
        

        # thuc hien tinh ti sai phan khi tien mot moc noi suy
        Z = [y[n + i + 1]]
        for j in range(2*i):
            Z.append(Z[j] - Z2[j])
        Z2 = Z.copy()
        Z1.append(Z[-1])

        #thuc hien tinh ti sai phan khi lui mot moc noi suy
        Z = [y[n - i]]
        for j in range(2*i + 1):
            Z.append(Z1[j] - Z[j])
        Z1 = Z.copy()
        Z2.append(Z[-1])
        print("Z1 =", Z1)
        print("Z2 =", Z2)

        # tinh he so bac chan cua da thuc
        giai_thua *= 2*i
        print("giai thua {}! =".format(2*i - 1), giai_thua)
        P1.append(np.concatenate((np.array([0]), P1[-1])) + (Z1[2*i] + Z2[2*i]) * Li[i] / (2 * giai_thua))
        print("P1 =", P1[-1])

        #tinh he so bac le cua da thuc
        giai_thua *= 2*i + 1
        print("giai thua {}! =".format(2*i), giai_thua)        
        P2.append(np.concatenate((np.array([0]),P2[-1])) + (Z1[2*i + 1] * Li[i]) / giai_thua)
        print("P2 =", P2[-1])
    
    #thuc hien them so le cac he so bac chan va bac le lai voi nhau
    for i in range(0, n + 1):
        P.append(P2[-1][i])
        P.append(P1[-1][i])
    return np.array(P)

def gia_tri_noi_suy_tai(P, x0):
    # tra ve gia tri cua y tai x0 
    n = int((x.shape[0] - 1) / 2)
    t = (x0 - x[n])/h
    u = t - 1/2
    return hoocne_quatient(P, u)[1]

def ve_do_thi_da_thuc(P, x, y):
    a = int(np.ndarray.min(x)) - 1
    b = int(np.ndarray.max(x)) + 1
    x_i = np.linspace(a, b, num = (b - a) * 20)
    y_i = gia_tri_noi_suy_tai(P, x_i)
    print(y_i.shape)
    plt.plot(x_i, y_i)
    plt.plot(x, y, "o")
    plt.xlabel("Truc X")
    plt.ylabel("Truc Y")
    plt.title("DO THI CUA DA THUC NOI SUY")
    plt.show()

def bieu_dien_da_thuc(P):
    da_thuc = ""
    for i in range(P.shape[0] - 1):
        da_thuc += "{}x^{} + ".format(round(P[i], 5), P.shape[0] - 2 - i)
    da_thuc += str(round(P[-1], 5))
    return da_thuc
    
x, y = doc_input("Data_test_Bessel.xlsx")
kieu_moc, x, y = kiem_tra_input(x, y)
print(kieu_moc)
if(kieu_moc == 2 and kiem_tra_chan_le(x) == 0):
    h = x[1] - x[0]
    print("thuc hien thuat toan stirling")
    P = bessel(x, y)
    print("===============================================")
    print("Ket thu qua sau khi thuc hien noi suy stirling:")
    print("He so cua da thuc P la: ",P)
    print("Da thuc noi suy theo t: ", bieu_dien_da_thuc(P))
    print("===============================================")
    ve_do_thi_da_thuc(P, x, y)
    x0 = float(input("Chon vi tri can tinh gia tri: "))
    if(x0 >= x[0] and x0 < x[-1]):
        print("gia tri can tinh nam trong khoang noi suy")
        print("gia tri cua y tai {} =".format(x0) , gia_tri_noi_suy_tai(P, x0))
    else:
        print("gia tri can tinh nam ngoai khoang noi suy")

