import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    gray = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/"+"LENNA.bmp", cv2.IMREAD_GRAYSCALE)                  #画像の読み込み

    n = 5                                           # 画素値の分割数

    pos = posterization(gray, n)
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/Result_9-4.bmp", pos)       #ポスタリゼーションした画像の出力
    result=cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/"+"/Result_9-4.bmp", cv2.IMREAD_GRAYSCALE) 
    cv2.imshow('result',result)
    cv2.imshow('gray',gray)
    k = cv2.waitKey(0)
    

def posterization(img, n):
    x = np.arange(256)                   #0,1,2...255までの整数が並んだ配列

    ibins = np.linspace(0, 255, n+1)     #LUTより入力は255/(n+1)で分割
    obins = np.linspace(0,255, n)        #LUTより出力は255/nで分割

    num=np.digitize(x, ibins)-1          #インプットの画素値をポスタリゼーションするために番号付けを行う
    num[255] = n-1                       #digitize処理で外れてしまう画素値255の番号を修正する

    y = np.array(obins[num], dtype=int)   #ポスタリゼーションするLUTを作成する
    pos_LUT(n, y)                         #LUTの図を作成
    pos = cv2.LUT(img, y)                 #ポスタリゼーションを行う

    return pos

#ポスタリゼーションのLUT図作成
def pos_LUT(n, y):
    x = np.arange(0,256,1)
    plt.plot(x,y)
    plt.savefig(os.path.dirname(os.path.abspath(__file__))+"/Result_9-4.png")

if __name__=='__main__':
    main()