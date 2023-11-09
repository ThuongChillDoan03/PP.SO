import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import sympy as sym
from Hamphutro import saiphan, bangsaiphan, mulConst, mulHorner, sumHorner, horner

def gauss1horner(x, y, value):
    n = len(x)          # độ dài data
    h = x[1] - x[0]     # bước nhảy
    # tính bảng sai phân
    table = bangsaiphan(x,y)
    # đưa các giá trị sai phân sẽ chọn vào một list
    list_sai_phan = []

    # áp dụng công thức
    if(n%2==1):
      #print("Số mốc lẻ")
      poly = [0] # phần tích đầu tiên là bậc 0 với giá trị là 0
      ans = [table[0][int(n/2)]]          # biến kết quả ans lần lượt là các hệ số của đa thức nội suy
      fact = 1
      list_sai_phan.append(table[0][int(n/2)])
      for i in range(1,n):
        fact = fact*i
        poly = mulHorner(poly, i, 1)
        ans =  sumHorner(ans, mulConst(poly,table[i][int((n-i)/2)]/fact))
        list_sai_phan.append(table[i][int((n-i)/2)]) # lấy giá trị sai phân

      # Tính giá trị đa thức tại value
      result = horner(ans, (value - x[int(n/2)]) / h)
    else:
      #print("Số mốc chẵn")
      poly = [0]
      ans = [table[0][int((n-1)/2)]]
      fact = 1
      list_sai_phan.append(table[0][int((n-1)/2)])
      for i in range(1,n):
        fact = fact*i
        poly = mulHorner(poly, i, 1)
        ans =  sumHorner(ans, mulConst(poly,table[i][int((n-i-1)/2)]/fact))
        list_sai_phan.append(table[i][int((n-i-1)/2)])
      
      # Tính giá trị đa thức tại value
      result = horner(ans, (value - x[int((n-1)/2)]) / h)
    print('Các sai phân đã chọn theo Gauss 1:', list_sai_phan)
    return ans, result


if __name__ == '__main__':
    print('Phương pháp Gauss 1')

    # đọc dữ liệu trực tiếp
    # x = [310, 320, 330, 340, 350, 360, 370]
    # y = [2.4914, 2.5052, 2.5185, 2.5315, 2.5441, 2.5563, 2.5687]
    # value = 345

    # đọc dữ liệu từ file
    f = pd.read_excel("Data_Gauss1.xlsx")
    b = np.asarray(f.astype(np.float64))
    b = b.T     #Data đầu vào dạng dọc (bỏ lệnh này nếu đang ở dạng ngang)
    x = b[0]
    y = b[1]
    print("X = ",x)
    print("Y = ",y)

    # x.reverse()
    # y.reverse()
    value = 345       #giá trị cần  tính


    # In bảng sai phân
    table = bangsaiphan(x,y)
    n = len(x)
    print('Bảng sai phân:')
    for i in range(n):
        print(x[i], end = "\t")
        for j in range(n-i):
            print(table[j][i], end = "\t")
        print("")

    print('-----------------------------------------')
    ans = gauss1horner(x, y, value)
    print('Hệ số đa thức theo t:', np.round(ans[0],4))
    print('Giá trị tại', value, 'là:', ans[1])



    # Kiểm tra kết quả:
    predict = []
    # đổi sang biến t
    t = []
    if(n%2==1):
      for ele_x in x:
        ele_t = (ele_x - x[int(n/2)]) / (x[1] - x[0])
        t.append(ele_t)
    else:
      for ele_x in x:
        ele_t = (ele_x - x[int((n-1)/2)]) / (x[1] - x[0])
        t.append(ele_t)
    
    for ele_t in t:
      ele_y = horner(ans[0], ele_t)
      predict.append(ele_y)

    print('-----------------------------------------')
    print('Kiểm tra đa thức:')
    print('Predict:', predict)
    print('True:', y)





    # Vẽ dữ liệu
    # plt.figure(dpi=60, figsize=(25,6))
    plt.plot(x, y, marker='o', label='Dữ liệu')

    # Vẽ đa thức nội suy
    # lấy ra một khoảng x để vẽ đồ thị
    x_plot = np.linspace(min(x),max(x), num = 100)
    # đổi biến x sang biến t:
    t_plot = []
    if(n%2==1):
      for ele_x in x_plot:
        ele_t = (ele_x - x[int(n/2)]) / (x[1] - x[0])
        t_plot.append(ele_t)
    else:
      for ele_x in x_plot:
        ele_t = (ele_x - x[int((n-1)/2)]) / (x[1] - x[0])
        t_plot.append(ele_t)
    # tính y_plot tương ứng với t_plot
    y_plot = []
    for t in t_plot:
      ele_y = horner(ans[0], t)
      y_plot.append(ele_y)

    plt.plot(x_plot, y_plot, label='Đa thức nội suy')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

