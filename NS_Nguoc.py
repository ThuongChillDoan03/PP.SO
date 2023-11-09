import numpy as np
import pandas as pd

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

def hoocne_product(x):
    #tich cua cac nghiem
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

def lay_khoang_song_anh(x, y):
    khoang_song_anh = list()
    song_anh = [0]
    n = x.shape[0]
    if y[0] < y[1]:
        sgn = 1
    else:
        sgn = -1
    for i in range(1, n):
        if(y[i - 1] < y[i] and sgn == -1) or (y[i - 1] > y[i] and sgn == 1):
            song_anh.append(i - 1)
            song_anh.append(sgn)
            khoang_song_anh.append(np.array(song_anh))
            song_anh = [i - 1]
            sgn = -sgn
    song_anh.append(n - 1)
    song_anh.append(sgn)
    khoang_song_anh.append(np.array(song_anh))
    return khoang_song_anh
            
def noi_suy_moc_bat_ki(x, y):
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

def ham_nguoc(x, y):
    P = noi_suy_moc_bat_ki(y, x)
    return hoocne_quatient(P, y0)[1]

def lap_newton_tien(x, y, y0):
    P = list()
    Z = list()
    P.append(np.array([y[0] - y0]))
    P.append(np.concatenate((np.array([0]) ,P[0])))
    Z.append(np.array([y[0]]))
    Z.append(np.array([y[1], y[1] - y[0]]))
    dentaY0 = y[1] - y[0]
    t1 = (y0 - y[0])/dentaY0
    t0 = t1
    giai_thua = 1
    n = y.shape[0]
    t = np.array(range(n))
    Li = hoocne_product(t)
    lan_lap = 0
    print("=======================================================")
    print("lan lap thu {}: {}".format(lan_lap, x[0] + t1 * h))
    for i in range(2, n):
        lan_lap += 1 
        giai_thua *= i
        z = [y[i]]
        for j in range(i):
            z.append(z[j] - Z[i - 1][j])
        Z.append(np.array(z))
        Fi = Z[-1][-1]
        P.append(np.concatenate((np.array([0]), P[i - 1])) + (Fi * Li[i])/giai_thua)
        t0 = t1
        t1 = (-1 / dentaY0) * hoocne_quatient(P[-1], t0)[1]
        print("lan lap thu {}: {}".format(lan_lap, x[0] + t1 * h))
        # if(abs(t1 - t0) < eps):
        #     break
    while(abs(t1 - t0) > eps):
        lan_lap += 1
        t0 = t1
        t1 = (-1 / dentaY0) * hoocne_quatient(P[-1], t0)[1]
        print("lan lap thu {}: {}".format(lan_lap, x[0] + t1 * h))
    print("=======================================================")
    return x[0] + t1 * h

def lap_newton_lui(x, y, y0):
    P = list()
    Z = list()
    P.append(np.array([y[0] - y0]))
    P.append(np.concatenate((np.array([0]) ,P[0])))
    Z.append(np.array([y[0]]))
    Z.append(np.array([y[1], y[1] - y[0]]))
    dentaY0 = y[1] - y[0]
    t1 = (y0 - y[0])/dentaY0
    t0 = t1
    giai_thua = 1
    n = y.shape[0]
    t = np.array(range(n))
    Li = hoocne_product(t)
    lan_lap = 0
    print("=======================================================")
    print("lan lap thu {}: {}".format(lan_lap, x[0] - t1 * h))
    for i in range(2, n):
        lan_lap += 1 
        giai_thua *= i
        z = [y[i]]
        for j in range(i):
            z.append(z[j] - Z[i - 1][j])
        Z.append(np.array(z))
        Fi = Z[-1][-1]
        P.append(np.concatenate((np.array([0]), P[i - 1])) + (Fi * Li[i])/giai_thua)
        t0 = t1
        t1 = -1 / dentaY0 * hoocne_quatient(P[-1], t0)[1]
        print("lan lap thu {}: {}".format(lan_lap, x[0] - t1 * h))
        # if(abs(t1 - t0) < eps):
        #     break
    while(abs(t1 - t0) > eps):
        lan_lap += 1
        t0 = t1
        t1 = -1 / (y[1] - y[0]) * hoocne_quatient(P[-1], t0)[1]
        print("lan lap thu {}: {}".format(lan_lap, x[0] - t1 * h))
    print("=======================================================")
    return x[0] - t1 * h

#doc input
x, y = doc_input("Data_test_NSNguoc.xlsx")
y0 = float(input("nhap y0: "))      #Nhập vào giá trị y0 để tính x tại đó.
kieu_moc, x, y= kiem_tra_input(x, y)
h = x[1] - x[0]

if(kieu_moc == 2):
    khoang_song_anh = lay_khoang_song_anh(x, y)
    for i in khoang_song_anh:
        print("({}, {})".format(x[i[0]], x[i[1]]))

    while(True):
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("======================")
        print("Cac khoang song anh:")
        j = 1
        for i in khoang_song_anh:
            if y0 >= np.ndarray.min(y[i[0]:i[1] + 1]) and y0 <= np.ndarray.max(y[i[0]:i[1] + 1]):
                print("khoang {}: ({}, {})".format(j, x[i[0]], x[i[1]]))
            else:
                khoang_song_anh.pop(j - 1)
            j += 1
        print("======================")
        chon_khoang = int(input("Chon khoang song anh muon tim nghiem (nhan 0 de thoat): "))
        if chon_khoang == 0:
            break
        print("==============================")
        print("Khoang song anh duoc su dung: (co {} moc noi suy)".format(khoang_song_anh[chon_khoang - 1][1] + 1 - khoang_song_anh[chon_khoang - 1][0]))
        print(x[khoang_song_anh[chon_khoang - 1][0]:khoang_song_anh[chon_khoang - 1][1] + 1])
        print(y[khoang_song_anh[chon_khoang - 1][0]:khoang_song_anh[chon_khoang - 1][1] + 1])
        print("==============================")
        index = 0
        if(khoang_song_anh[chon_khoang - 1][2] == 1):
            for i in range(khoang_song_anh[chon_khoang - 1][0], khoang_song_anh[chon_khoang - 1][1]):
                if(y0 >= y[i] and y0 <= y[i + 1]):
                    index = i
                    break
        else:
            for i in range(khoang_song_anh[chon_khoang - 1][0], khoang_song_anh[chon_khoang - 1][1]):
                if(y0 <= y[i] and y0 >= y[i + 1]):
                    index = i
                    break
        print("============================")
        print("chon chuc nang muon su dung:")
        print("1. Lap newton")          # Lặp tốt hơn cho mốc cách đều
        print("2. Ham nguoc")           # Mốc bất kì nhưng chậm
        print("============================")
        chon_chuc_nang = int(input("Chon chuc nang: "))
        
        # su dung phuong phap lap newton
        if(chon_chuc_nang == 1):
            n = x.shape[0]
            eps = float(input("nhap epsilon: "))
            if(index < n / 2):
                xbar = np.array(x[index:n])
                ybar = np.array(y[index:n])
                print("===================================")
                print("Cac moc noi suy duoc su dung:")
                print("x = {}".format(xbar))
                print("y = {}".format(ybar))
                print("===================================")
                print("gia tri cua x khi y = {} la x = {}".format(y0 ,lap_newton_tien(xbar, ybar, y0)))
            else:
                xbar = np.flip(np.array(x[0:index + 2])) 
                ybar = np.flip(np.array(y[0:index + 2]))
                print("===================================")
                print("Cac moc noi suy duoc su dung:")
                print("x = {}".format(xbar))
                print("y = {}".format(ybar))
                print("===================================")
                print("gia tri cua x khi y = {} la x = {}".format(y0 ,lap_newton_lui(xbar, ybar, y0)))


        #su dung phuong phap tim ham nguoc
        elif(chon_chuc_nang == 2):
            so_moc = int(input("Chon so moc muon su dung: "))
            start = khoang_song_anh[chon_khoang - 1][0]
            end = khoang_song_anh[chon_khoang - 1][1] + 1
            if(so_moc >= khoang_song_anh[chon_khoang - 1][1] - khoang_song_anh[chon_khoang - 1][0] + 1):
                pass
            else:
                n = int(so_moc / 2)
                start = index - n
                end = index + (so_moc - n)
                if(start < khoang_song_anh[chon_khoang - 1][0]):
                    end += (khoang_song_anh[chon_khoang - 1][0] - start)
                    start = khoang_song_anh[chon_khoang - 1][0]
                if(end > khoang_song_anh[chon_khoang - 1][1]):
                    start -= (end - khoang_song_anh[chon_khoang - 1][1])
                
            print("({}, {})".format(start, end))
            xbar = np.array(x[start:end])
            ybar = np.array(y[start:end])
            print("===================================")
            print("Cac moc noi suy duoc su dung:")
            print("x = {}".format(xbar))
            print("y = {}".format(ybar))
            print("===================================")
            print("hệ số của hàm ngược là: {}".format(noi_suy_moc_bat_ki(xbar, ybar)))
            print("gia tri cua x khi y = {} la x = {}".format(y0 ,ham_nguoc(xbar, ybar))) 

        else:
            print("Chuc nang khong hop le!! Yeu cau nhap lai!!")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")