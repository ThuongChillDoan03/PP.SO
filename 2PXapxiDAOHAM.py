from logging import exception
import numpy as np
import pandas as pd
import math

def input_data():
    #  Data đầu vào dạng dọc, X, Y cùng file
    inp = pd.read_excel("Data_test_daoham.xlsx")
    b = np.asarray(inp.astype(np.float64))
    b = b.T
    data_x = b[0]
    data_y = b[1]

    # dt_x = pd.read_excel("inputX.txt")
    # data_x = np.asarray(dt_x.astype(np.float64))
    # dt_y = pd.read_excel("inputY.txt")
    # data_x = np.asarray(dt_y.astype(np.float64))

    check_input(data_x, data_y)
    x = float(input("Tinh dao ham tai X = "))
    dx = float(data_x[1] - data_x[0])
    return [data_x, data_y, x, dx]

def check_input (data_x, data_y):
    # tra ve 1 khi input hop le va 0 khi input khong hop le
    # kiem tra kich thuoc du lieu
    if (data_x.shape[0] != data_y.shape[0]):
        print("Kich thuoc X, Y khong bang nhau!")
        return 0
    #kiem tra so luong moc noi suy
    if len(data_x)-1 < 2:
        print("So luong moc noi suy qua it!")
        return 0
    # kiem tra du lieu trung
    for i in data_x:
        if (np.where(data_x == i)[0].shape[0] > 1):
             print("Du lieu cua data_x o cac vi tri ", np.where(data_x == i)[0], " trung nhau")
             return 0
    # kiem tra khoang cach cac moc noi suy
    dx = data_x[1] - data_x[0]
    for i in range(2, data_x.size):
        # SAI SO KHOANG CACH
        if abs(data_x[i] - data_x[i - 1] - dx) > 1e-4:
            raise Exception("Cac moc phai cach deu nhau!")
            return 0
    # input hop le
    print("Input hop le!\n")
    return 1

#---------------------------------- SAI PHAN TIEN -------------------------------------------------
#Su dung sai phan tien tinh dao ham cap 1
def forward_difference_first_order(data_x, data_y, x, dx):
    idx = np.where(data_x == x)
    if idx[0].size != 0:
        if idx[0]+2 > len(data_x)-1:
            print("Khong the su dung phuong phap sai phan tien tinh dao ham cap 1 tai 2 diem cuoi!")
        else:
            return (-data_y[idx[0][0] + 2] + 4*data_y[idx[0][0] + 1] - 3*data_y[idx[0][0]])/(2 * dx)
    else:
        print("Diem X khong thuoc cac moc noi suy da cho!")
    
#Sai phan tien tinh dao ham cap 2
def forward_difference_second_order(data_x, data_y, x, dx):
    idx = np.where(data_x == x)
    if idx[0].size != 0:
        if idx[0]+2 > len(data_x)-1:
            print("Khong the su dung phuong phap sai phan tien tinh dao ham cap 2!")
        else:
            return  (data_y[idx[0][0] + 2] - 2 * data_y[idx[0][0] + 1] +  data_y[idx[0][0]])/(dx * dx)
    else:
        print("Diem X khong thuoc cac moc noi suy da cho!")

#----------------------------------- SAI PHAN LUI ---------------------------------------------
#Sai phan lui tinh dao ham cap 1
def backward_difference_first_order(data_x, data_y, x, dx):
    idx = np.where(data_x == x)
    if idx[0].size != 0:
        if idx[0] == 1 or idx[0] ==0:
            print("Khong the su dung phuong phap sai phan lui tinh dao ham cap 1 tai 2 diem dau!")
        else:
            return (3*data_y[idx[0][0]] - 4*data_y[idx[0][0] - 1] + data_y[idx[0][0]-2])/(2 * dx)
    else:
        print("Diem X khong thuoc cac moc noi suy da cho!")

#Sai phan lui tinh dao ham cap 2
def backward_difference_second_order(data_x, data_y, x, dx):
    idx = np.where(data_x == x)
    if idx[0].size != 0:
        if idx[0] <= 1:
            print("Khong the su dung phuong phap sai phan lui tinh dao ham cap 2 tai 2 diem dau tien!")
        else:
            return  (data_y[idx[0][0] - 2] - 2 * data_y[idx[0][0] - 1] + data_y[idx[0][0]])/(dx * dx)
    else:
        print("Diem X khong thuoc cac moc noi suy da cho!")
        
#---------------------------------SAI PHAN GIUA XAP XI P2-----------------------------------------------
#Sai phan giua tinh dao ham cap 1
def centered_difference_first_order_P2(data_x, data_y, x, dx):

    idx = np.where(data_x == x)
    if idx[0].size != 0:
        if idx[0]==0 or idx[0]==-1:
            print("Tinh dao ham tai diem dau tien va diem cuoi cung khong the su dung phuong phap sai phan giua!")
        else:
            return (data_y[idx[0][0] + 1] - data_y[idx[0][0] - 1])/(2 * dx)
    else:
        print("Diem X khong thuoc cac moc noi suy da cho!")

#Sai phan giua tinh dao ham cap 2
def centered_difference_second_order_P2(data_x, data_y, x, dx):

    idx = np.where(data_x == x)

    if idx[0].size != 0:
        #Kiem tra vi tri cua X trong data_x
        if idx[0] == 0 or idx[0]==-1:
            print("Tinh dao ham tai diem dau tien va diem cuoi cung khong the su dung phuong phap sai phan giua!")
        else:
            return (data_y[idx[0][0] + 1] - 2 * data_y[idx[0][0]] + data_y[idx[0][0] - 1])/(dx * dx)
    else:
        print("Diem X khong thuoc cac moc noi suy da cho!")

#--------------------------------------------------------------------------------
def test_forward_difference():
    data_x, data_y, x, dx  = input_data()
    dy = forward_difference_first_order(data_x, data_y, x, dx)
    print ("Tinh theo sai phan tien:")
    print("Dao ham cap 1 tai X = {} : {}".format(x, dy))
    dy2 = forward_difference_second_order(data_x, data_y, x, dx)
    print("Dao ham cap 2 tai X = {} : {}".format(x, dy2))
    print ("\n")
        
def test_backward_difference():

    data_x, data_y, x, dx = input_data()
    dy = backward_difference_first_order(data_x, data_y, x, dx)
    print ("Tinh theo sai phan lui:")
    print("Dao ham cap 1 tai X = {} : {}".format(x, dy))
    dy2 = backward_difference_second_order(data_x, data_y, x, dx)
    print("Dao ham cap 2 tai X = {} : {}".format(x, dy2))
    print ("\n")
    
def test_centered_difference_P2():
    
    data_x, data_y, x, dx = input_data()
    dy = centered_difference_first_order_P2(data_x, data_y, x, dx)
    print ("Tinh theo sai phan giua xap xi P2(x)")
    print("Dao ham cap 1 tai X = {} : {}".format(x, dy))
    dy2 = centered_difference_second_order_P2(data_x, data_y, x, dx)
    print("Dao ham cap 2 tai X = {} : {}".format(x, dy2))
    print("\n")
    

test_forward_difference()
test_backward_difference()
test_centered_difference_P2()