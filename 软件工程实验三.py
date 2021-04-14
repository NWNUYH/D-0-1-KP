#!/usr/bin/env python
# coding: utf-8

#软件工程实验二
#---------------------------------------导入必要的包，定义所需的函数---------------------------------------
#导入时间包，便于记录动态规划法和回溯法所用时间
import time
#导入pandas，需使用dataframe类型
import pandas as pd
#导入可视化包,用于绘制散点图
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False  

#函数fun1去除一维列表one_list中的空项，返回无空项的一维列表
def fun1(one_list): 
    return [i for i in one_list if(len(str(i))!=0)]

#函数fun2将一个长度为n的一维列表的项进行划分 ，每个子列表中包含m个项，返回n/m行，m列的二维列表
def fun2(one_list,m=6):  
    return [one_list[i:i+m] for i in range(len(one_list)) if i%m==0]

#函数fun3将一个字符串中遇到的所有符号替换为空格，再将由空格分隔的几个值的序列（str类型）转化为列表，调用函数fun1去除一维列表one_list中的空项，返回处理后的列表
def fun3(one_str):
    one_str = one_str.replace(","," ").replace("."," ").replace("="," ").replace("*"," ")
    one_str = one_str.split(" ")
    one_str = fun1(one_str)
    return one_str

#动态规划法
def backpack(n, c, w, v):
    #初始化二维数组，用于记录背包中个数为i，重量为j时能获得的最大价值
    result = [[0 for i in range(c+1)] for i in range(n+1)]
    #循环将数组进行填充
    for i in range(1, n+1):
        for j in range(1, c+1):
            if j < w[i-1]:
                result[i][j] = result[i-1][j]
            else:
                result[i][j] = max(result[i-1][j], result[i-1][j-w[i-1]] + v[i-1])
    return result

#回溯法
def backtrack(i):
    global bestV,curW,curV
    if i>=n:
        if bestV<curV:
            bestV=curV
    else:
        if curW+w[i]<=c:
            curW+=w[i]
            curV+=v[i]
            backtrack(i+1)
            curW-=w[i]
            curV-=v[i]
        backtrack(i+1)


#---------------------------------------读取数据,处理数据---------------------------------------
#读取数据集,处理数据
def Read_data():
    x=input("请输入要读取的数据集:idkp/sdkp/udkp/wdkp\n")
    file = open(r""+x+"1-10.txt",mode='r')
    content = file.read()
    #去除content中的换行符
    content = content.split("\n")
    #调用fun1去除列表content中的空项
    content = fun1(content)
    #去除new_content中的首尾项
    content = content[1:-1]
    #调用fun2将数据分块
    content=fun2(content,m=6)
    #将二维列表转换为DataFrame
    df = pd.DataFrame(content)
    #获取第x行第1列的值,此时是str类型
    x=input("请输入要读取哪一组数据:1-10\n")
    x=int(x)-1
    KP = df.loc[x,1]
    #调用fun3处理字符串KP
    KP = fun3(KP)
    #从字符串KP中准备提取出物品总数amount
    global amount
    amount = int(KP[4])*int(KP[5])
    print("物品总数:" + str(amount))
    #从字符串KP中准备提取出背包容量cubage
    global cubage
    cubage = int(KP[-1])
    print("背包容量:" + str(cubage))
    #提取出profit值
    #获取第x行第3列的profit的值,此时是str类型
    profit = df.loc[x,3]
    #调用fun3处理字符串profit
    profit = fun3(profit)
    #提取出weight值
    #获取第x行第5列的weight的值,此时是str类型
    weight = df.loc[x,5]
    #调用fun3处理字符串weight
    weight = fun3(weight)
    #将列表元素profit,weight类型由object转换为int64
    global profit_int
    profit_int = list(map(int, profit)) #profit = [int(i) for i in profit]同
    print("价值为:"+str(profit_int))
    global weight_int
    weight_int = list(map(int, weight)) #weight = [int(i) for i in weight]同
    print("重量为:"+str(weight_int))

#---------------------------------------绘制散点图---------------------------------------
#绘制散点图
def Scatter():
    #将两个列表合并为dataframe类型，便于绘制散点图
    #List转DataFrame
    global profit_weight
    profit_weight = pd.DataFrame(profit_int, columns=['profit'])
    #多个List合并成一个DataFrame
    profit_weight = pd.concat([profit_weight, pd.DataFrame(weight_int,columns=['weight'])],axis=1)
    #绘制散点图
    profit_weight.plot(x='weight',y='profit',kind='scatter')
    #x坐标轴文本
    plt.xlabel('重量')
    #y坐标轴文本
    plt.ylabel('价值')
    #图片标题
    plt.title('重量与价值散点图')
    #显示网格
    plt.grid(True)
    #显示图形
    plt.show()

#---------------------------------------第三项的价值:重量比非递增排序---------------------------------------
#按第三项的价值:重量比非递增排序
def Descending_sort():
#调用fun2将列表项三项为一项子列表项
    profit_list=fun2(profit_int,m=3)
    weight_list=fun2(weight_int,m=3)
    #将二维列表profit_list转换为DataFrame
    profit_df = pd.DataFrame(profit_list)
    #将二维列表weight_list转换为DataFrame
    weight_df = pd.DataFrame(weight_list)
    #将两个dataframe合并为一个dataframe
    profit_weight_df = pd.concat([profit_df,weight_df],axis=1)
    profit_weight_df.columns=['first_profit','scecond_profit','third_profit','first_weight','scecond_weight','third_weight']
    #计算项集第三项的价值:重量比
    third_profit_weight = profit_weight_df["third_profit"]/profit_weight_df["third_weight"]
    #将第三项的价值:重量比插入dataframe
    profit_weight_df.insert(6,"third_profit_weight",third_profit_weight)
    #非递增排序
    profit_weight_df.sort_values(by = ['third_profit_weight'],ascending = False,inplace=True)
    print(profit_weight_df)
    
#---------------------------------------自主选择动态规划法或回溯法，并写入txt文件---------------------------------------
#自主选择动态规划法或回溯法，并写入txt文件
def Solve_write_data():
    choice = input('''请选择：动态规划法------1\n
                            回溯法----------2\n''')
    if choice == '1':
        start = time.time()
        result = backpack(amount, cubage, weight_int, profit_int)
        end = time.time()
        print("最优解为：" + str(result[amount][cubage]) + "\n")
        print("共耗时:" + str(end - start) + " s")
        #写入txt文件
        output_file = open(r"Dynamic_KnapSack_output.txt",mode='w')
        output_file = output_file.write("最优解为：" + str(result[amount][cubage]) + "\n" + "共耗时:" + str(end - start) + " s")
    elif choice == '2':
        n = amount
        c = cubage
        w = weight_int
        v = profit_int
        start = time.time()
        backtrack(0)
        end = time.time()
        print("最优解为：" + str(bestV)+ "\n")
        print("共耗时:" + str(end - start) + " s")
        #写入txt文件
        output_file = open(r"Back_KnapSack_output.txt",mode='w')
        output_file = output_file.write("最优解为：" + str(bestV) + "\n" + "共耗时:" + str(end - start) + " s")
    else:
        print("无此项选择")

#---------------------------------------main()函数---------------------------------------
def main():
    while(True):
        menu()
        option = input("请选择:")
        if option == '1':
            Read_data()
        elif option == '2':
            Scatter()
        elif option == '3': 
            Descending_sort()
        elif option == '4': 
            Solve_write_data()
        else:
            print("退出!")
            break

#---------------------------------------菜单---------------------------------------
def menu():
    print('''
******************************菜单******************************
        1 读取数据集,处理数据
        2 绘制散点图
        3 按第三项的价值:重量比非递增排序
        4 自主选择动态规划法或回溯法，并写入txt文件
        5 退出
****************************************************************
    ''')
#---------------------------------------程序入口---------------------------------------
main()


# In[1]:


import numpy as np
import random
import matplotlib.pyplot as plt
##初始化,N为种群规模，n为染色体长度
def init(N,n):
    C = []
    for i in range(N):
        c = []
        for j in range(n):
            a = np.random.randint(0,2)
            c.append(a)
        C.append(c)
    return C


##评估函数
# x(i)取值为1表示被选中，取值为0表示未被选中
# w(i)表示各个分量的重量，v（i）表示各个分量的价值，w表示最大承受重量
def fitness(C,N,n,W,V,w):
    S = []##用于存储被选中的下标
    F = []## 用于存放当前该个体的最大价值
    for i in range(N):
        s = []
        h = 0  # 重量
        f = 0  # 价值
        for j in range(n):
            if C[i][j]==1:
                if h+W[j]<=w:
                    h=h+W[j]
                    f = f+V[j]
                    s.append(j)
        S.append(s)
        F.append(f)
    return S,F

##适应值函数,B位返回的种族的基因下标，y为返回的最大值
def best_x(F,S,N):
    y = 0
    x = 0
    B = [0]*N
    for i in range(N):
        if y<F[i]:
            x = i
        y = F[x]
        B = S[x]
    return B,y

## 计算比率
def rate(x):
    p = [0] * len(x)
    s = 0
    for i in x:
        s += i
    for i in range(len(x)):
        p[i] = x[i] / s
    return p

## 选择
def chose(p, X, m, n):
    X1 = X
    r = np.random.rand(m)
    for i in range(m):
        k = 0
        for j in range(n):
            k = k + p[j]
            if r[i] <= k:
                X1[i] = X[j]
                break
    return X1

##交配
def match(X, m, n, p):
    r = np.random.rand(m)
    k = [0] * m
    for i in range(m):
        if r[i] < p:
            k[i] = 1
    u = v = 0
    k[0] = k[0] = 0
    for i in range(m):
        if k[i]:
            if k[u] == 0:
                u = i
            elif k[v] == 0:
                v = i
        if k[u] and k[v]:
            # print(u,v)
            q = np.random.randint(n - 1)
            # print(q)
            for i in range(q + 1, n):
                X[u][i], X[v][i] = X[v][i], X[u][i]
            k[u] = 0
            k[v] = 0
    return X

##变异
def vari(X, m, n, p):
    for i in range(m):
        for j in range(n):
            q = np.random.rand()
            if q < p:
                X[i][j] = np.random.randint(0,2)

    return X

m = 8##规模
N = 800  ##迭代次数
Pc = 0.8 ##交配概率
Pm = 0.05##变异概率
V =[125,821,946,359,987,1346,258,763,1021,107,622,729,474,744,1218,150,490,640,260,497,757,225,490,715,563,658,1221,1003,1007,2010,341,594,935,316,441,757,653,898,1551,243,817,1060,457,895,1352,709,852,1561,561,604,1165,348,511,859,541,915,1456,156,1067,1223,666,777,1443,799,972,1771,572,807,1379,1015,1055,2070,531,745,1276,567,638,1205,280,966,1246,608,864,1472,483,1095,1578,172,534,706,693,1040,1733,162,990,1152,645,1029,1674,522,991,1513,942,958,1900,270,323,593,252,563,815,192,999,1191,831,856,1687,326,389,715,200,275,475,365,761,1126,357,516,873,466,966,1432,677,1067,1744,131,864,995,413,956,1369,573,875,1448,331,454,785,126,286,412,477,653,1130,304,863,1167,809,981,1790,366,964,1330,152,886,1038,240,413,653,927,998,1925,151,684,835,270,777,1047,134,1002,1136,541,794,1335,395,1052,1447,270,527,797,247,1083,1330,326,999,1325,201,342,543,190,567,757,568,573,1141,588,883,1471,876,920,1796,270,887,1157,552,704,1256,129,161,290,427,579,1006,914,937,1851,310,484,794,770,851,1621,245,790,1035,273,320,593,171,471,642,328,642,970,698,885,1583,728,1025,1753,637,840,1477,564,1005,1569,216,573,789,145,688,833,703,744,1447,299,897,1196,876,956,1832,488,548,1036,322,606,928,494,496,990,413,993,1406,691,761,1452,915,969,1884,376,864,1240,193,457,650,341,741,1082,370,497,867]
W =[25,721,725,259,887,934,158,663,777,7,522,528,374,644,664,50,390,410,160,397,549,125,390,478,463,558,630,903,907,976,241,494,714,216,341,365,553,798,1265,143,717,791,357,795,970,609,752,862,461,504,926,248,411,583,441,815,1017,56,967,1013,566,677,715,699,872,1203,472,707,860,915,955,1156,431,645,902,467,538,911,180,866,1017,508,764,833,383,995,1302,72,434,483,593,940,1431,62,890,893,545,929,1371,422,891,1217,842,858,1419,170,223,365,152,463,464,92,899,910,731,756,892,226,289,369,100,175,262,265,661,672,257,416,426,366,866,1166,577,967,1093,31,764,788,313,856,921,473,775,1096,231,354,359,26,186,202,377,553,921,204,763,825,709,881,1053,266,864,869,52,786,787,140,313,400,827,898,1561,51,584,591,170,677,746,34,902,917,441,694,775,295,952,964,170,427,564,147,983,1032,226,899,1108,101,242,260,90,467,501,468,473,693,488,783,803,776,820,1018,170,787,878,452,604,1020,29,61,65,327,479,610,814,837,1314,210,384,500,670,751,1408,145,690,797,173,220,385,71,371,385,228,542,694,598,785,1138,628,925,1130,537,740,1023,464,905,946,116,473,587,45,588,598,603,644,1112,199,797,813,776,856,1019,388,448,612,222,506,537,394,396,558,313,893,1058,591,661,831,815,869,1613,276,764,809,93,357,394,241,641,675,270,397,439]
n = len(W)##染色体长度
w = 60143

C = init(m, n)
S,F  = fitness(C,m,n,W,V,w)
B ,y = best_x(F,S,m)
Y =[y]
for i in range(N):
    p = rate(F)
    C = chose(p, C, m, n)
    C = match(C, m, n, Pc)
    C = vari(C, m, n, Pm)
    S, F = fitness(C, m, n, W, V, w)
    B1, y1 = best_x(F, S, m)
    if y1 > y:
        y = y1
    Y.append(y)
print("最大值为：",y)

plt.plot(Y)
plt.show()


# In[ ]:





# In[ ]:




