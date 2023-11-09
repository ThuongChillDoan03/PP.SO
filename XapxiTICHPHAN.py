import numpy as np
import pandas as pd

### NOTE_ : TẤT CẢ CÁC CÔNG THỨC ĐƯỢC SỬ DỤNG DƯỚI DẠNG TỔNG QUÁT (KO XÉT CT ĐỊA PHƯƠNG)
### INPUT1-1: LÀ SỬ DỤNG n0 MỐC ĐƯỢC SUY RA TỪ CÔNG THỨC SAI SỐ
### INPUT1-2: LÀ SỬ DỤNG n MỐC NHẬP LIỆU ĐẦU VÀO


denta = [0.5e-5, 1e-4, 2e-2, 1e-2]  #lấy giá trị nhỏ để xấp xỉ đạo hàm

# hàm tính giá trị f(x)
###__________________INPUT_1 (Nhập liệu hàm và sai số, số mốc muốn muốn chọn)______________________###
def f(x):
    return 1/(1+x**2)
# cận trên
a = 0
#cận dưới
b = 3
# sai số
eps = 0.5e-8
# số mốc
n = 10

###__________________________________________________________________________________###

# tính đạo hàm cấp 1 của f(x)
def df(x):
    return (f(x + denta[0]) - f(x - denta[0])) / (2*denta[0])

# tính đạo hàm cấp 2 của f(x)
def ddf(x):
    return (df(x + denta[1]) - df(x - denta[1])) / (2*denta[1])

# tính đạo hàm cấp 3 của f(x)
def dddf(x):
    return (ddf(x + denta[2]) - ddf(x - denta[2])) / (2*denta[2])

# tính đạo hàm cấp 4 của f(x)
def ddddf(x):
    return (dddf(x + denta[3]) - dddf(x - denta[3])) / (2*denta[3])


# tính max của đạo hàm cấp 2 trên đoạn [a, b]
def max_ddf(a, b):
    max = 0
    for i in np.arange(a, b, 1e-2):
        if np.abs(ddf(i)) > max:
            max = np.abs(ddf(i))
    return max

# tính max của đạo hàm cấp 4 trên đoạn [a, b]
def max_ddddf(a, b):
    max = 0
    for i in np.arange(a, b, 1e-2):
        if np.abs(dddf(i)) > max:
            max = np.abs(dddf(i))
    return max

# nhân đa thức bằng hoocne
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

# chia đa thức bằng hoocne
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

# đọc input 2 từ file
def doc_input2 (ten_file):
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
            if(x.shape[0] % 2 == 0):
                print("so moc noi suy la chan")
                return 1, x, y
            else:
                print("so moc noi suy la le")
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
            if(x.shape[0] % 2 == 0):
                print("so moc noi suy la chan")
                return 1, x, y
            else:
                print("so moc noi suy la le")
                return 2, x, y

    return 1, x, y


# tính các mốc cần dùng để tính tích phân theo hình thang
def mocs_hinh_thang(a, b, n):
    mocs = []
    h = (b - a) / n
    for i in range(n + 1):
        mocs.append(a + i * h)
    x = np.array(mocs)
    y = f(x)
    return x, y

# tính các mốc cần dùng để tính tích phân theo simpson
def mocs_simpson(a, b, n):
    mocs = []
    h = (b - a) / (2 * n)
    for i in range(2 * n + 1):
        mocs.append(a + i * h)
    x = np.array(mocs)
    y = f(x)
    return x, y


# tính tích phân theo hình thang với input 1-1 
def tich_phan_hinh_thang_input1_1(a, b, eps):
    n0 = int(np.sqrt((b - a)**3 * abs(max_ddf(a, b)) / (12 * eps))) + 2
    x, y = mocs_hinh_thang(a, b, n0 - 1)
    h = x[1] - x[0]
    sai_so = (b - a) * abs(max_ddf(a, b)) * h**2 / 12
    print("giá trị lớn nhất của đạo hàm bậc 2: ", max_ddf(a, b))
    print("Số môc được sử dụng: ", n0)
    print("Khoảng cách giữa các mốc: ",h)
    return h/2*(y[0] + y[-1] + 2 * np.sum(y[1:-1])), sai_so

# tính tích phân theo hình thang với input 1-2
def tich_phan_hinh_thang_input1_2(a, b, n):
    x, y = mocs_hinh_thang(a, b, n - 1)
    h = x[1] - x[0]
    sai_so = (b - a) * abs(max_ddf(a, b)) * h**2 / 12
    print("Số môc được sử dụng: ", n)
    print("Khoảng cách giữa các mốc: ",h)
    return h/2*(y[0] + y[-1] + 2 * np.sum(y[1:-1])), sai_so

# tính tích phân theo simpson với input 1-1
def tich_phan_simpson_input1_1(a, b, eps):
    n0 = int(((b - a)**5 * abs(max_ddddf(a, b)) / (180 * eps))**(1/4) / 2) + 2
    if n0 % 2 == 0:
        print("Số mốc là số chắn nên được cộng thêm 1 !!!")
        n0 += 1
    x, y = mocs_simpson(a, b, n0 - 1)
    h = x[1] - x[0]
    sai_so = (b - a) * abs(max_ddddf(a, b)) * h**4 / 180
    print("giá trị lớn nhất của đạo hàm bậc 4: ", max_ddddf(a, b))
    print("Số môc được sử dụng: ", 2 * n0 - 1)
    print("Khoảng cách giữa các mốc: ",h)
    return h/3*(y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2])), sai_so

# tính tích phân theo simpson với input 1-2
def tich_phan_simpson_input1_2(a, b, n):
    x, y = mocs_simpson(a, b, n - 1)
    h = x[1] - x[0]
    sai_so = (b - a) * abs(max_ddddf(a, b)) * h**4 / 180
    print("Số môc được sử dụng: ", 2 * n - 1)
    print("Khoảng cách giữa các mốc: ",h)
    return h/3*(y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2])), sai_so


# tính tích phân bằng công thức hình thang với input là các mốc x, y và đánh giá sai số eps
def tich_phan_hinh_thang_input2(x, y):
    h = x[1] - x[0]
    Ih = h/2*(y[0] + y[-1] + 2 * np.sum(y[1:-1]))
    I2h = h*(y[0] + y[-1] + 2*np.sum(y[2:-2:2]))
    eps = abs(Ih - I2h)/3
    print("Số môc được sử dụng: ", x.shape[0])
    print("Khoảng cách giữa các mốc: ",h)
    print("giá trị của I2h: ", I2h)
    print("giá trị của Ih: ", Ih)
    return Ih, eps

# tính tích phân bằng công thức simpson với input là các mốc x, y và đánh giá sai số eps
def tich_phan_simpson_input2(x, y):
    h = x[1] - x[0]
    Ih = h/3*(y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2]))
    I2h = 2*h/3*(y[0] + y[-1] + 4*np.sum(y[2:-2:4]) + 2*np.sum(y[4:-4:4]))
    eps = abs(Ih - I2h)/15
    print("Số môc được sử dụng: ", x.shape[0])
    print("Khoảng cách giữa các mốc: ",h)
    print("giá trị của I2h: ", I2h)
    print("giá trị của Ih: ", Ih)
    return Ih, eps


# tính hệ số của tích phân bằng newton cotes
def newton_cotes_coefficient(k):
    # trả về một mảng là hệ số của công thức newton cotes
    # k là số lượng mốc
    IP = list()
    omega = hoocne_product(np.linspace(0, k - 1, k))[-1]
    for i in range(k):
        P = hoocne_quatient(omega, i)[0] / np.linspace(k, 1, k)
        product = 1
        for j in range(k):
            if(j != i):
                product *= (i - j)
        P = np.concatenate((P, np.array([0])))
        IP.append(hoocne_quatient(P, k - 1)[1] / product)
    return np.array(IP) / (k-1)

# chạy chương trình với input 1
print("===============================")
result1_1, eps1_1 = tich_phan_hinh_thang_input1_1(a, b, eps)
print("tích phân theo hình thang với eps = {}: ".format(eps), result1_1)
print("sai số thu được: ", eps1_1)
print("-----------------------------")
result2_1, eps2_1 = tich_phan_simpson_input1_1(a, b, eps)
print("tích phân theo simpson với eps = {}: ".format(eps), result2_1)
print("sai số thu được: ", eps2_1)
print("===============================")
result1_2, eps1_2 = tich_phan_hinh_thang_input1_2(a, b, n)
print("tích phân theo hình thang với n = {}: ".format(n), result1_2)
print("sai số thu được: ", eps1_2)
if n % 2 == 0:
    print("n phải là số lẻ để tính được tích phân theo simpson")
else:
    print("-----------------------------")
    result2_2, eps2_2 = tich_phan_simpson_input1_2(a, b, n)
    print("tích phân theo simpson với n = {}: ".format(n), result2_2)
    print("sai số thu được: ", eps2_2)


# chạy chương trình với input 2
x, y = doc_input2("Data_test_tichphan.xlsx")
check, x, y = kiem_tra_input(x, y) 
if check == 1:
    print("khong the tinh tich phan")
elif check == 2:
    result1, eps1 = tich_phan_hinh_thang_input2(x, y)
    print("tích phân theo hình thang: ", result1)
    print("sai số theo lưới đều: ", eps1)
    print("-----------------------------")
    result2, eps2 = tich_phan_simpson_input2(x, y)
    print("tích phân theo simpson: ", result2)
    print("sai số theo lưới đều: ", eps2)
else:
    print("các mốc không sắp xếp hoặc không cách đều")


#in ra hệ số của công thức newton cotes
k = int(input("nhập số lượng mốc (để lấy ra hệ số của công thức Newton-Cotes): "))
print("hệ số của công thức newton cotes với {} mốc: ".format(k), newton_cotes_coefficient(k))


